"""
Facade Pattern implementation.
"""
from patterns.chain_of_responsibility import ValidationChain
from patterns.observer import EventPublisher
from patterns.command import SagaOrchestrator, ReserveSeatCommand, CreateEnrollmentCommand, UpdateScheduleCommand
from models.course import EnrollmentRequest, ValidationResult, EnrollmentResult, DropResult, EnrollmentEvent, CourseOffering, EnrollmentRepository, Schedule, Enrollment, ScheduleEntry

class EnrollmentFacade:
    """Coordinates validation, persistence, and event publication."""
    def __init__(self, event_publisher: EventPublisher, offering: CourseOffering, repository: EnrollmentRepository, schedule: Schedule):
        self.validator = ValidationChain()
        self.event_publisher = event_publisher
        self.offering = offering
        self.repository = repository
        self.schedule = schedule
        
    def enroll(self, studentId: str, offeringId: str) -> EnrollmentResult:
        """Facade method to handle the enrollment workflow."""
        print(f"Facade: Attempting to enroll {studentId} in offering {offeringId}...")
        
        req = EnrollmentRequest(studentId, offeringId)
        
        # 1. Coordinate Validation
        if self.validator.validate(req) == ValidationResult.FAILED:
            print("Facade: Enrollment failed due to validation errors.")
            return EnrollmentResult.FAILURE
            
        # 2. Coordinate Persistence via Saga Orchestrator
        orchestrator = SagaOrchestrator()
        orchestrator.steps.append(ReserveSeatCommand(self.offering))
        orchestrator.steps.append(CreateEnrollmentCommand(self.repository, Enrollment(studentId, offeringId)))
        orchestrator.steps.append(UpdateScheduleCommand(self.schedule, ScheduleEntry(studentId, offeringId)))
        
        if not orchestrator.run():
            print("Facade: Saga transaction failed.")
            return EnrollmentResult.FAILURE
            
        # 3. Coordinate Event Publication
        self.event_publisher.publish(EnrollmentEvent("ENROLLMENT_SUCCESS", {"student_id": studentId, "course_id": offeringId}))
        return EnrollmentResult.SUCCESS

    def drop(self, studentId: str, offeringId: str) -> DropResult:
        """Facade method to handle the course dropping workflow."""
        # Simple drop implementation for proof-of-concept
        self.offering.releaseSeat()
        self.repository.delete(Enrollment(studentId, offeringId))
        self.schedule.removeEntry(ScheduleEntry(studentId, offeringId))
        
        # Event publication
        self.event_publisher.publish(EnrollmentEvent("COURSE_DROPPED", {"student_id": studentId, "course_id": offeringId}))
        return DropResult.SUCCESS
