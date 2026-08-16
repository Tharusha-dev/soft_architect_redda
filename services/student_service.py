"""
Student Module implementation.
"""
from patterns.facade import EnrollmentFacade
from typing import Dict
from models.course import Course
from models.user import Student

class StudentService:
    """Service handling student-specific business logic."""
    def __init__(self, enrollment_facade: EnrollmentFacade):
        self.enrollment_facade = enrollment_facade

    def browse_courses(self, courses_db: Dict[str, Course]):
        """Browses the course catalog."""
        print("\n--- Course Catalog ---")
        for cid, course in courses_db.items():
            print(f"[{cid}] {course.name} - {course.description} (Seats available: {course.get_available_seats()})")
        print("----------------------\n")

    def enroll_in_course(self, student_id: str, course_id: str):
        """Attempts to enroll the student in a course using the Facade."""
        self.enrollment_facade.enroll(student_id, course_id)

    def drop_course(self, student_id: str, course_id: str):
        """Attempts to drop a course for the student using the Facade."""
        self.enrollment_facade.drop(student_id, course_id)
        
    def view_schedule(self, student_id: str, students_db: Dict[str, Student], courses_db: Dict[str, Course]):
        """Builds and displays a personal schedule view."""
        student = students_db.get(student_id)
        if not student:
            return
        print(f"\n--- Schedule for {student.name} ---")
        for cid in student.enrolled_courses:
            course = courses_db.get(cid)
            print(f"{course.name} - {course.schedule}")
        print("----------------------------------\n")
