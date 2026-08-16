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
        # Simplistic proof-of-concept
        print(f"ValidationChain [Prerequisite]: Passed.")
        return self.forward(req)

class CapacityValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
        # Simplistic proof-of-concept
        print(f"ValidationChain [Capacity]: Passed.")
        return self.forward(req)

class TimeConflictValidator(EnrollmentValidator):
    def validate(self, req: EnrollmentRequest) -> ValidationResult:
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
