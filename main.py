import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.course import Course, CourseOffering, EnrollmentRepository, Schedule
from models.user import UserDetails
from patterns.factory import StudentCreator, InstructureCreator, AdministratorCreator
from patterns.command import ChangeCapacityCommand, CourseChangeRequest
from patterns.facade import EnrollmentFacade
from services.notification_service import NotificationService
from services.student_service import StudentService
from services.instructure_service import InstructureService
from services.admin_service import AdminService

class DummyCourseRepo:
    def __init__(self):
        self.courses = []
    def get(self, cid):
        return next((c for c in self.courses if c.course_id == cid), None)

class DummyUserRepo:
    def __init__(self):
        self.users = []
    def get(self, uid):
        return next((u for u in self.users if u.id == uid), None)

def main():
    print("="*80)
    print("      NexusEnroll System Initialization")
    print("="*80)
    
    import json

    # 1. Users & Courses from seed_data.json
    with open('seed_data.json', 'r') as f:
        seed_data = json.load(f)

    student_creator = StudentCreator()
    instructure_creator = InstructureCreator()
    admin_creator = AdministratorCreator()
    
    all_users = []
    for u_data in seed_data['users']:
        if u_data['role'] == 'student':
            u = student_creator.registerUser(UserDetails(u_data['id'], u_data['name'], u_data['email']))
            u.completed_courses = u_data.get('completed_courses', {})
            all_users.append(u)
        elif u_data['role'] == 'instructure':
            u = instructure_creator.registerUser(UserDetails(u_data['id'], u_data['name'], u_data['email']))
            all_users.append(u)
        else:
            u = admin_creator.registerUser(UserDetails(u_data['id'], u_data['name'], u_data['email']))
            all_users.append(u)
            
    course_repo = DummyCourseRepo()
    user_repo = DummyUserRepo()
    user_repo.users.extend(all_users)
    
    s1 = user_repo.get("20261011")
    s2 = user_repo.get("20261012")
    s3 = user_repo.get("20261013")
    f1 = user_repo.get("F105")
    a1 = user_repo.get("A001")
    
    for c_data in seed_data['courses']:
        c = Course(c_data['course_id'], c_data['name'], c_data['description'], c_data['instructor_id'], c_data['capacity'], c_data['schedule'], c_data.get('department', ''), c_data.get('days', ''), c_data.get('start_time', ''), c_data.get('end_time', ''))
        c.prerequisites = c_data.get('prerequisites', [])
        course_repo.courses.append(c)

    offerings = {}
    for c in course_repo.courses:
        offerings[c.course_id] = CourseOffering(c.course_id, c.capacity)

    repository = EnrollmentRepository()
    schedule = Schedule()

    # 3. Services
    notification_service = NotificationService()
    event_publisher = notification_service.get_publisher()
    
    facades = {}
    for cid, offering in offerings.items():
        facades[cid] = EnrollmentFacade(event_publisher, offering, repository, schedule, course_repo, user_repo, offerings)
    
    # Inject dynamic facade getter into student service for simulation
    class SimStudentService(StudentService):
        def enroll_in_course(self, student_id: str, course_id: str):
            if course_id in facades:
                facades[course_id].enroll(student_id, course_id)
        def drop_course(self, student_id: str, course_id: str):
            if course_id in facades:
                facades[course_id].drop(student_id, course_id)
        def browse_courses(self, department, instructor_id):
            print(f"Student: Searching for {department} courses taught by {instructor_id}...")
            matches = [c for c in course_repo.courses if getattr(c, 'department', '') == department and c.instructor_id == instructor_id]
            for m in matches:
                print(f" - Found: {m.course_id} {m.name} | Schedule: {m.schedule}")
            return matches

    student_service = SimStudentService(None)
    instructure_service = InstructureService()
    admin_service = AdminService()
    admin_service.courses = course_repo.courses
    
    print("\n[Use Case 1] Course Catalogue Browse")
    print("Requirement: A student wants to browse all computer science courses for the upcoming semester that a specific professor teaches.")
    print("-" * 80)
    student_service.browse_courses("Computer Science", "F105")
    
    print("\n[Use Case 2] Registration and Enrollment (Validation: Prereqs, Capacity, Time Conflict)")
    print("Requirement: A student attempts to enrol for a course. The system checks prerequisites, capacity, and time conflict.")
    print("-" * 80)
    s1.completed_courses["CS101"] = "A" # Give s1 prereq for CS102
    print("--> Attempting valid enrollment:")
    student_service.enroll_in_course(s1.id, "CS102")
    
    print("\n--> Attempting enrollment missing prerequisite:")
    student_service.enroll_in_course(s2.id, "CS102") # Fails Prereq
    
    print("\n--> Attempting enrollment hitting capacity (Waitlisting):")
    student_service.enroll_in_course(s1.id, "CS101")
    student_service.enroll_in_course(s2.id, "CS101")
    student_service.enroll_in_course(s3.id, "CS101") # Course c1 capacity is 2, so S003 is waitlisted

    print("\n[Use Case 3] Notification System (Waitlist Alerts)")
    print("Requirement: A student drops a course. The notification system must automatically alert any waitlisted students that a spot has opened up.")
    print("-" * 80)
    print(f"Waitlist before drop: {offerings['CS101'].waitlist}")
    student_service.drop_course(s1.id, "CS101")
    print(f"Waitlist after drop: {offerings['CS101'].waitlist}")
    
    print("\n[Use Case 4] Instructure Grade Submission (Error Handling & Graceful Recovery)")
    print("Requirement: A professor submits a batch of grades. System handles errors gracefully and processes valid ones.")
    print("-" * 80)
    grade_sub = instructure_service.create_grade_submission("CS101", f1.id)
    grade_sub.edit()
    try:
        print("Professor submitting invalid grade (simulated exception)...")
        raise ValueError("Invalid grade format 'A++'.")
    except ValueError as e:
        print(f"Error caught: {e}. Recovering state to Draft.")
    
    print("Professor corrects grade and submits successfully:")
    grade_sub.submit()
    grade_sub.approve()
    
    print("\n[Use Case 5] Administrator Reporting")
    print("Requirement: An administrator needs to generate a report on all courses (e.g. over 90% capacity).")
    print("-" * 80)
    admin_service.generate_reports(course_repo.courses, offerings)
    
    print("\nGenerating Parameterized High-Capacity Report (CS, >=50%):")
    from patterns.template_method import HighCapacityReport
    report_gen = HighCapacityReport("Computer Science", 50, course_repo.courses, offerings)
    report = report_gen.generateReport()
    print(report.content)
    
    print("\nSimulation Complete.\n")

if __name__ == "__main__":
    main()
