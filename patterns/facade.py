"""
Facade Pattern implementation.
"""
from patterns.chain_of_responsibility import ValidationChain
from patterns.observer import EventPublisher
from patterns.command import SagaOrchestrator, ReserveSeatCommand, CreateEnrollmentCommand, UpdateScheduleCommand
from models.course import EnrollmentRequest, ValidationResult, EnrollmentResult, DropResult, EnrollmentEvent, CourseOffering, EnrollmentRepository, Schedule, Enrollment, ScheduleEntry

class EnrollmentFacade:
    """Coordinates validation, persistence, and event publication."""
    def __init__(self, event_publisher: EventPublisher, offering: CourseOffering, repository: EnrollmentRepository, schedule: Schedule, course_repository=None, user_repository=None, offerings=None):
        self.validator = ValidationChain()
        self.event_publisher = event_publisher
        self.offering = offering
        self.repository = repository
        self.schedule = schedule
        self.course_repository = course_repository
        self.user_repository = user_repository
        self.offerings = offerings
        
    def enroll(self, studentId: str, offeringId: str) -> EnrollmentResult:
        """Facade method to handle the enrollment workflow."""
        print(f"Facade: Attempting to enroll {studentId} in offering {offeringId}...")
        
        student = self.user_repository.get(studentId) if self.user_repository else None
        course = self.course_repository.get(offeringId) if self.course_repository else None
        
        # Build enrolled schedules context
        enrolled_schedules = []
        if student and self.course_repository:
            for c_id in student.enrolled_courses:
                c = self.course_repository.get(c_id)
                if c:
                    enrolled_schedules.append(c.schedule)
                    
        req = EnrollmentRequest(studentId, offeringId, student, course, self.offering, self.schedule, enrolled_schedules)
        
        if self.validator.validate(req) == ValidationResult.FAILED:
            print("Facade: Enrollment failed due to validation errors.")
            if self.offering and course and self.offering.enrolled_count >= course.capacity:
                self.offering.addToWaitlist(studentId)
                self.event_publisher.publish(EnrollmentEvent("WAITLIST_JOINED", {"student_id": studentId, "course_id": offeringId}))
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
        self.offering.releaseSeat()
        self.repository.delete(Enrollment(studentId, offeringId))
        self.schedule.removeEntry(ScheduleEntry(studentId, offeringId))
        
        self.event_publisher.publish(EnrollmentEvent("COURSE_DROPPED", {"student_id": studentId, "course_id": offeringId}))
        
        # Waitlist handling
        if self.offering.waitlist:
            next_student = self.offering.waitlist.pop(0)
            self.event_publisher.publish(EnrollmentEvent("WAITLIST_PROMOTED", {"student_id": next_student, "course_id": offeringId}))
            
        return DropResult.SUCCESS
