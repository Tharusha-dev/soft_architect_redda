"""
NexusEnroll System Simulation - Main Entry Point.
Executes the primary use cases to demonstrate the architectural design.
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.course import Course, CourseOffering, EnrollmentRepository, Schedule
from models.user import UserDetails
from patterns.factory import StudentCreator, FacultyCreator, AdministratorCreator
from patterns.command import ChangeCapacityCommand, CourseChangeRequest
from services.notification_service import NotificationService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from services.faculty_service import FacultyService
from services.admin_service import AdminService

def main():
    print("="*60)
    print("      NexusEnroll System Initialization")
    print("="*60)
    
    # 1. Use Factory Method to create Users
    student_creator = StudentCreator()
    faculty_creator = FacultyCreator()
    admin_creator = AdministratorCreator()
    
    s1 = student_creator.registerUser(UserDetails("S001", "Alice Smith", "alice@nexus.edu"))
    s2 = student_creator.registerUser(UserDetails("S002", "Bob Jones", "bob@nexus.edu"))
    f1 = faculty_creator.registerUser(UserDetails("F001", "Prof. Alan Turing", "alan@nexus.edu"))
    a1 = admin_creator.registerUser(UserDetails("A001", "Admin Grace", "grace@nexus.edu"))
    
    # 2. Create Dummy Course Data
    c1 = Course("CS101", "Intro to CS", "Python programming.", f1.id, 2, "Mon 10AM")
    offering = CourseOffering(c1.course_id, c1.capacity)
    repository = EnrollmentRepository()
    schedule = Schedule()
    
    # 3. Initialize Services
    notification_service = NotificationService()
    event_publisher = notification_service.get_publisher()
    
    enrollment_service = EnrollmentService(event_publisher, offering, repository, schedule)
    student_service = StudentService(enrollment_service.get_facade())
    faculty_service = FacultyService()
    admin_service = AdminService()
    
    print("\n[Use Case 1] Student Enrollment (Facade, Chain of Responsibility, Saga Orchestrator)")
    print("-" * 60)
    student_service.enroll_in_course(s1.id, c1.course_id)
    student_service.enroll_in_course(s2.id, c1.course_id)
    # Third enrollment fails because capacity is 2
    student_service.enroll_in_course("S003", c1.course_id)
    
    print("\n[Use Case 2] Student Dropping Course (Observer Pattern Notification)")
    print("-" * 60)
    student_service.drop_course(s1.id, c1.course_id)
    
    print("\n[Use Case 3] Faculty Grade Submission (State Pattern Lifecycle)")
    print("-" * 60)
    grade_sub = faculty_service.create_grade_submission(c1.course_id, f1.id)
    grade_sub.edit()
    grade_sub.submit()
    grade_sub.edit() # Failed edit
    grade_sub.approve()
    grade_sub.edit() # Failed edit
    
    print("\n[Use Case 4] Faculty Course Change Request (Command Pattern)")
    print("-" * 60)
    change_cmd = ChangeCapacityCommand(c1, 5)
    request = CourseChangeRequest("REQ001", c1.course_id, f1.id, change_cmd)
    
    faculty_service.submit_course_change_request(request, admin_service)
    admin_service.approve_course_change_request("REQ001")
    
    print("\n[Use Case 5] Admin Reporting (Template Method Pattern)")
    print("-" * 60)
    admin_service.generate_reports()
    
    print("\nSimulation Complete.\n")

if __name__ == "__main__":
    main()
