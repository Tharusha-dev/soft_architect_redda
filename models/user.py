"""
Models for NexusEnroll Users.
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from enum import Enum

class Role(Enum):
    STUDENT = "STUDENT"
    INSTRUCTURE = "INSTRUCTURE"
    ADMINISTRATOR = "ADMINISTRATOR"

class UserDetails:
    def __init__(self, id: str, name: str, email: str, role: Role = None):
        self.id = id
        self.name = name
        self.email = email
        self.role = role

class User(ABC):
    """Abstract base class representing a NexusEnroll user."""
    def __init__(self, id: str, name: str, email: str):
        self._id = id
        self._name = name
        self._email = email
        self.is_active = True
        
    def deactivate(self):
        self.is_active = False
        
    def reactivate(self):
        self.is_active = True

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def email(self) -> str:
        return self._email

    @abstractmethod
    def getRole(self) -> Role:
        """Returns the role of the user."""
        pass

class Student(User):
    """Represents a student user in the NexusEnroll system."""
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email)
        self.enrolled_courses: List[str] = []
        self.completed_courses: Dict[str, str] = {} # course_id: grade
        self.waitlisted_courses: List[str] = []
        
    def getRole(self) -> Role:
        return Role.STUDENT

class Instructure(User):
    """Represents a instructure user in the NexusEnroll system."""
    def __init__(self, id: str, name: str, email: str):
        super().__init__(id, name, email)
        self.teaching_courses: List[str] = []
        
    def getRole(self) -> Role:
        return Role.INSTRUCTURE

class Administrator(User):
    """Represents an administrator user in the NexusEnroll system."""
    def getRole(self) -> Role:
        return Role.ADMINISTRATOR
