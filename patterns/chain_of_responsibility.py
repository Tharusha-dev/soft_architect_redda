"""
Chain of Responsibility Pattern implementation.
"""
from abc import ABC, abstractmethod
from models.user import Student
from models.course import Course, EnrollmentRequest, ValidationResult

class EnrollmentValidator(ABC):
    """Abstract handler for the ValidationChain."""
    def __init__(self):
        self.next: 'EnrollmentValidator' = None
        
    def setNext(self, v: 'EnrollmentValidator') -> 'EnrollmentValidator':
        """Sets the next validator in the chain."""
        self.next = v
        return v
        
    @abstractmethod
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        """Validates the request."""
        pass
        
    def forward(self, req: EnrollmentRequest) -> ValidationResult:
        """Forwards the request to the next handler if successful."""
        if self.next:
            return self.next.validate(req)
        return ValidationResult.PASSED

class PrerequisiteValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        if req.student and req.course:
            for prereq in req.course.prerequisites:
                if prereq not in req.student.completed_courses:
                    print(f"ValidationChain [Prerequisite]: Failed. Missing {prereq}.")
                    return ValidationResult.FAILED
        print(f"ValidationChain [Prerequisite]: Passed.")
        return self.forward(req)

class CapacityValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        if req.offering and req.course:
            if req.offering.enrolled_count >= req.course.capacity:
                print(f"ValidationChain [Capacity]: Failed. Course is full.")
                # addToWaitlist happens in facade
                return ValidationResult.FAILED
        print(f"ValidationChain [Capacity]: Passed.")
        return self.forward(req)

from models.course import check_time_conflict
class TimeConflictValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        if req.course and req.enrolled_schedules:
            for sched in req.enrolled_schedules:
                if check_time_conflict(req.course.schedule, sched):
                    print(f"ValidationChain [TimeConflict]: Failed. Conflict detected.")
                    return ValidationResult.FAILED
        print(f"ValidationChain [TimeConflict]: Passed. No time conflict detected.")
        return self.forward(req)

class ValidationChain:
    """The client interface that assembles and triggers the chain."""
    def __init__(self):
        self.first = PrerequisiteValidator()
        capacity = CapacityValidator()
        time_conflict = TimeConflictValidator()
        self.first.setNext(capacity).setNext(time_conflict)
        
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        """Starts the validation process."""
        return self.first.validate(req)
