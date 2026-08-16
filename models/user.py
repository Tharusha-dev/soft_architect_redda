"""
Models for NexusEnroll Users.
"""
from abc import ABC, abstractmethod
from typing import List, Dict

class User(ABC):
    """Abstract base class representing a NexusEnroll user."""
    def __init__(self, user_id: str, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

    @abstractmethod
    def get_role(self) -> str:
        """Returns the role of the user."""
        pass

class Student(User):
    """Represents a student user in the NexusEnroll system."""
    def __init__(self, user_id: str, name: str, email: str):
        super().__init__(user_id, name, email)
        self.enrolled_courses: List[str] = []
        self.completed_courses: Dict[str, str] = {} # course_id: grade
        self.waitlisted_courses: List[str] = []
        
    def get_role(self) -> str:
        return "Student"

class Faculty(User):
    """Represents a faculty user in the NexusEnroll system."""
    def __init__(self, user_id: str, name: str, email: str):
        super().__init__(user_id, name, email)
        self.teaching_courses: List[str] = []
        
    def get_role(self) -> str:
        return "Faculty"

class Administrator(User):
    """Represents an administrator user in the NexusEnroll system."""
    def get_role(self) -> str:
        return "Administrator"
