"""
Models for NexusEnroll Courses.
"""
from typing import List, Any, Dict
from enum import Enum

class RequestStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

class ValidationResult(Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"

class EnrollmentResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class DropResult(Enum):
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"

class EnrollmentEvent:
    def __init__(self, type: str, payload: Dict[str, Any]):
        self.type = type
        self.payload = payload

class EnrollmentRequest:
    def __init__(self, student_id: str, course_id: str):
        self.student_id = student_id
        self.course_id = course_id

class Enrollment:
    def __init__(self, student_id: str, course_id: str):
        self.student_id = student_id
        self.course_id = course_id

class Course:
    """Represents a course in NexusEnroll."""
    def __init__(self, course_id: str, name: str, description: str, instructor_id: str, capacity: int, schedule: str):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.instructor_id = instructor_id
        self.capacity = capacity
        self.schedule = schedule
        self.prerequisites: List[str] = []
        
    def setDescription(self, d: str):
        self.description = d

    def addPrerequisite(self, c: 'Course'):
        self.prerequisites.append(c.course_id)

    def setCapacity(self, n: int):
        self.capacity = n

class CourseOffering:
    def __init__(self, course_id: str, capacity: int):
        self.course_id = course_id
        self.capacity = capacity
        self.enrolled_count = 0

    def reserveSeat(self):
        if self.enrolled_count < self.capacity:
            self.enrolled_count += 1
            return True
        return False

    def releaseSeat(self):
        if self.enrolled_count > 0:
            self.enrolled_count -= 1

class ScheduleEntry:
    def __init__(self, student_id: str, course_id: str):
        self.student_id = student_id
        self.course_id = course_id

class Schedule:
    def __init__(self):
        self.entries: List[ScheduleEntry] = []

    def addEntry(self, entry: ScheduleEntry):
        self.entries.append(entry)

    def removeEntry(self, entry: ScheduleEntry):
        self.entries = [e for e in self.entries if not (e.student_id == entry.student_id and e.course_id == entry.course_id)]

class EnrollmentRepository:
    def __init__(self):
        self.enrollments: List[Enrollment] = []

    def save(self, e: Enrollment):
        self.enrollments.append(e)

    def delete(self, e: Enrollment):
        self.enrollments = [enr for enr in self.enrollments if not (enr.student_id == e.student_id and enr.course_id == e.course_id)]
