"""
Enrollment Service acting as a shared business logic container.
"""
from patterns.facade import EnrollmentFacade
from patterns.observer import EventPublisher
from models.course import CourseOffering, EnrollmentRepository, Schedule

class EnrollmentService:
    """Provides access to the EnrollmentFacade for processing enrollments."""
    def __init__(self, event_publisher: EventPublisher, offering: CourseOffering, repository: EnrollmentRepository, schedule: Schedule):
        self.facade = EnrollmentFacade(event_publisher, offering, repository, schedule)
        
    def get_facade(self) -> EnrollmentFacade:
        return self.facade
