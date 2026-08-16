"""
Enrollment Service acting as a shared business logic container.
"""
from patterns.facade import EnrollmentFacade
from patterns.observer import EventPublisher
from typing import Dict
from models.course import Course
from models.user import Student

class EnrollmentService:
    """Provides access to the EnrollmentFacade for processing enrollments."""
    def __init__(self, event_publisher: EventPublisher, courses_db: Dict[str, Course], students_db: Dict[str, Student]):
        self.facade = EnrollmentFacade(event_publisher, courses_db, students_db)
        
    def get_facade(self) -> EnrollmentFacade:
        return self.facade
