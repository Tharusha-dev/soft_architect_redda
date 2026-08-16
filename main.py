"""
NexusEnroll System Simulation - Main Entry Point.
Executes the primary use cases to demonstrate the architectural design.
"""
import sys
import os

# Add the current directory to sys.path to allow imports to work directly when running python main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.course import Course, CourseChangeRequest
from patterns.factory import StudentCreator, FacultyCreator, AdministratorCreator
from patterns.command import ChangeCapacityCommand
from patterns.state import DraftState, PendingState, SubmittedState
from services.notification_service import NotificationService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from services.faculty_service import FacultyService
from services.admin_service import AdminService

def main():
    print("="*60)
    print("      NexusEnroll System Initialization")
    print("="*60)
    
    # In-memory Databases (Simulated persistence)
    users_db = {}
    courses_db = {}
    
    # 1. Use Factory Method to create Users
    student_creator = StudentCreator()
    faculty_creator = FacultyCreator()
    admin_creator = AdministratorCreator()
    
    s1 = student_creator.create_user("S001", "Alice Smith", "alice@nexus.edu")
    s2 = student_creator.create_user("S002", "Bob Jones", "bob@nexus.edu")
    s3 = student_creator.create_user("S003", "Charlie Brown", "charlie@nexus.edu")
    f1 = faculty_creator.create_user("F001", "Prof. Alan Turing", "alan@nexus.edu")
    a1 = admin_creator.create_user("A001", "Admin Grace", "grace@nexus.edu")
    
    for u in [s1, s2, s3, f1, a1]:
        users_db[u.user_id] = u
        
    # Give S1 the prerequisite so she can enroll in CS201 later if she wants, though she won't in the simulation
    s1.completed_courses["CS101"] = "A"
    
    # 2. Create Dummy Courses
    c1 = Course("CS101", "Intro to Computer Science", "Learn Python programming.", f1.user_id, 2, "Mon/Wed 10AM")
    c2 = Course("CS201", "Data Structures", "Advanced data structures and algorithms.", f1.user_id, 30, "Tue/Thu 1PM")
    c2.prerequisites.append("CS101") # Bob does not have this prereq
    
    courses_db[c1.course_id] = c1
    courses_db[c2.course_id] = c2
    
    # 3. Initialize Shared Services
    notification_service = NotificationService()
    event_publisher = notification_service.get_publisher()
    
    enrollment_service = EnrollmentService(event_publisher, courses_db, users_db)
    student_service = StudentService(enrollment_service.get_facade())
    faculty_service = FacultyService()
    admin_service = AdminService()
    
    print("\n[Use Case 1] Student Enrollment (Facade & Chain of Responsibility)")
    print("-" * 60)
    # Bob tries to enroll in CS201 but fails prerequisite validation
    student_service.enroll_in_course(s2.user_id, c2.course_id)
    
    # Alice enrolls in CS101 successfully
    student_service.enroll_in_course(s1.user_id, c1.course_id)
    
    # Bob enrolls in CS101 successfully (Takes the 2nd and final seat)
    student_service.enroll_in_course(s2.user_id, c1.course_id)
    
    # Charlie tries to enroll in CS101 but fails capacity validation (only 2 seats)
    student_service.enroll_in_course(s3.user_id, c1.course_id)
    
    print("\n[Use Case 2] Student Dropping Course (Observer Pattern Notification)")
    print("-" * 60)
    # Alice drops CS101, Waitlist and Advisor observers should react
    student_service.drop_course(s1.user_id, c1.course_id)
    
    print("\n[Use Case 3] Faculty Grade Submission (State Pattern Lifecycle)")
    print("-" * 60)
    # Faculty creates grade submission
    grade_sub = faculty_service.create_grade_submission(c1.course_id, f1.user_id)
    
    grade_sub.edit({"S002": "A"}) # Edit in Draft
    grade_sub.submit()            # Draft -> Pending
    grade_sub.edit({"S002": "A+"})# Edit in Pending causes revert to Draft
    grade_sub.submit()            # Draft -> Pending
    grade_sub.approve()           # Pending -> Submitted
    grade_sub.edit({"S002": "B"}) # Fails, already finalized
    
    print("\n[Use Case 4] Faculty Course Change Request (Command Pattern)")
    print("-" * 60)
    # Increase capacity of CS101 to 5 using Command pattern
    change_cmd = ChangeCapacityCommand(c1, 5)
    request = CourseChangeRequest("REQ001", c1.course_id, f1.user_id, change_cmd)
    
    # Faculty submits it
    faculty_service.submit_course_change_request(request, admin_service)
    
    # Admin reviews and approves it, executing the command
    admin_service.approve_course_change_request("REQ001")
    
    print("\n[Use Case 5] Admin Reporting (Template Method Pattern)")
    print("-" * 60)
    # Generate structured reports
    admin_service.generate_enrollment_statistics()
    admin_service.generate_course_popularity()
    
    print("\nSimulation Complete.\n")

if __name__ == "__main__":
    main()
