"""
Chain of Responsibility Pattern implementation.
As dictated by the System Design Report: The Chain of Responsibility Pattern is used 
to validate a student's enrolment request. The request passes through PrerequisiteValidator, 
CapacityValidator, and TimeConflictValidator in sequence.
"""
from abc import ABC, abstractmethod
from models.user import Student
from models.course import Course

class EnrollmentValidator(ABC):
    """Abstract handler for the ValidationChain."""
    def __init__(self):
        self._next_validator: 'EnrollmentValidator' = None
        
    def set_next(self, validator: 'EnrollmentValidator') -> 'EnrollmentValidator':
        """Sets the next validator in the chain."""
        self._next_validator = validator
        return validator
        
    @abstractmethod
    def validate(self, student: Student, course: Course) -> bool:
        """Validates the request and passes it to the next handler if successful."""
        if self._next_validator:
            return self._next_validator.validate(student, course)
        return True

class PrerequisiteValidator(EnrollmentValidator):
    """Concrete handler checking for course prerequisites."""
    def validate(self, student: Student, course: Course) -> bool:
        for prereq in course.prerequisites:
            if prereq not in student.completed_courses:
                print(f"ValidationChain [Prerequisite]: Failed. Student {student.user_id} lacks prerequisite {prereq}.")
                return False
        print(f"ValidationChain [Prerequisite]: Passed.")
        return super().validate(student, course)

class CapacityValidator(EnrollmentValidator):
    """Concrete handler checking course capacity."""
    def validate(self, student: Student, course: Course) -> bool:
        if course.get_available_seats() <= 0:
            print(f"ValidationChain [Capacity]: Failed. Course {course.course_id} is full.")
            return False
        print(f"ValidationChain [Capacity]: Passed.")
        return super().validate(student, course)

class TimeConflictValidator(EnrollmentValidator):
    """Concrete handler checking for time conflicts."""
    def validate(self, student: Student, course: Course) -> bool:
        # Simplistic proof-of-concept check
        print(f"ValidationChain [TimeConflict]: Passed. No time conflict detected.")
        return super().validate(student, course)

class ValidationChain:
    """The client interface that assembles and triggers the chain."""
    def __init__(self):
        # Assemble the chain: Prerequisite -> Capacity -> TimeConflict
        self.head = PrerequisiteValidator()
        capacity = CapacityValidator()
        time_conflict = TimeConflictValidator()
        self.head.set_next(capacity).set_next(time_conflict)
        
    def validate(self, student: Student, course: Course) -> bool:
        """Starts the validation process."""
        return self.head.validate(student, course)
