"""
Factory Method Pattern implementation for creating Users.
"""
from abc import ABC, abstractmethod
from models.user import User, Student, Instructure, Administrator, UserDetails, Role

class UserCreator(ABC):
    """Abstract creator class for Factory Method pattern."""
    
    @abstractmethod
    def createUser(self, details: UserDetails) -> User:
        """Factory method to create a user."""
        pass
        
    def registerUser(self, details: UserDetails) -> User:
        """Template-like method that uses the factory method."""
        user = self.createUser(details)
        print(f"Registered new {user.getRole().value}: {user.name}")
        return user

class StudentCreator(UserCreator):
    """Concrete creator for Student objects."""
    def createUser(self, details: UserDetails) -> User:
        return Student(details.id, details.name, details.email)

class InstructureCreator(UserCreator):
    """Concrete creator for Instructure objects."""
    def createUser(self, details: UserDetails) -> User:
        return Instructure(details.id, details.name, details.email)

class AdministratorCreator(UserCreator):
    """Concrete creator for Administrator objects."""
    def createUser(self, details: UserDetails) -> User:
        return Administrator(details.id, details.name, details.email)
