"""
Factory Method Pattern implementation for creating Users.
As dictated by the System Design Report: The Factory Method Pattern is used by the
account-management functionality to create different types of NexusEnroll users.
"""
from abc import ABC, abstractmethod
from models.user import User, Student, Faculty, Administrator

class UserCreator(ABC):
    """Abstract creator class for Factory Method pattern."""
    @abstractmethod
    def create_user(self, user_id: str, name: str, email: str) -> User:
        """Factory method to create a user."""
        pass

class StudentCreator(UserCreator):
    """Concrete creator for Student objects."""
    def create_user(self, user_id: str, name: str, email: str) -> User:
        return Student(user_id, name, email)

class FacultyCreator(UserCreator):
    """Concrete creator for Faculty objects."""
    def create_user(self, user_id: str, name: str, email: str) -> User:
        return Faculty(user_id, name, email)

class AdministratorCreator(UserCreator):
    """Concrete creator for Administrator objects."""
    def create_user(self, user_id: str, name: str, email: str) -> User:
        return Administrator(user_id, name, email)
