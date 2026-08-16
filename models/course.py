"""
Models for NexusEnroll Courses.
"""
from typing import List, Any

class Course:
    """Represents a course offering in NexusEnroll."""
    def __init__(self, course_id: str, name: str, description: str, instructor_id: str, capacity: int, schedule: str):
        self.course_id = course_id
        self.name = name
        self.description = description
        self.instructor_id = instructor_id
        self.capacity = capacity
        self.schedule = schedule
        self.prerequisites: List[str] = []
        self.enrolled_students: List[str] = []
        self.waitlisted_students: List[str] = []
        
    def get_available_seats(self) -> int:
        """Calculates and returns the number of available seats."""
        return self.capacity - len(self.enrolled_students)

class CourseChangeRequest:
    """Represents a request from faculty to change course details."""
    def __init__(self, request_id: str, course_id: str, faculty_id: str, command: Any):
        self.request_id = request_id
        self.course_id = course_id
        self.faculty_id = faculty_id
        self.command = command # Command pattern instance
        self.status = "Pending"
