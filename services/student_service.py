"""
Student Module implementation.
"""
from patterns.facade import EnrollmentFacade
from typing import Dict
from models.course import Course

class StudentService:
    """Service handling student-specific business logic."""
    def __init__(self, enrollment_facade: EnrollmentFacade):
        self.enrollment_facade = enrollment_facade

    def enroll_in_course(self, student_id: str, course_id: str):
        """Attempts to enroll the student in a course using the Facade."""
        self.enrollment_facade.enroll(student_id, course_id)

    def drop_course(self, student_id: str, course_id: str):
        """Attempts to drop a course for the student using the Facade."""
        self.enrollment_facade.drop(student_id, course_id)
