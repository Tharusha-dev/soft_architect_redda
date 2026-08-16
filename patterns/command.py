"""
Command Pattern implementation.
As dictated by the System Design Report: The Command Pattern is used to encapsulate 
course-change requests (UpdateDescriptionCommand, AddPrerequisiteCommand, ChangeCapacityCommand).
"""
from abc import ABC, abstractmethod
from models.course import Course

class Command(ABC):
    """Abstract Command interface."""
    @abstractmethod
    def execute(self):
        pass
        
    @abstractmethod
    def undo(self):
        pass

class UpdateDescriptionCommand(Command):
    """Concrete command to update a course description."""
    def __init__(self, course: Course, new_description: str):
        self.course = course
        self.new_description = new_description
        self.old_description = course.description
        
    def execute(self):
        self.course.description = self.new_description
        print(f"Command executed: Course {self.course.course_id} description updated.")
        
    def undo(self):
        self.course.description = self.old_description
        print(f"Command undone: Course {self.course.course_id} description reverted.")

class AddPrerequisiteCommand(Command):
    """Concrete command to add a course prerequisite."""
    def __init__(self, course: Course, prerequisite_id: str):
        self.course = course
        self.prerequisite_id = prerequisite_id
        
    def execute(self):
        if self.prerequisite_id not in self.course.prerequisites:
            self.course.prerequisites.append(self.prerequisite_id)
            print(f"Command executed: Added prerequisite {self.prerequisite_id} to {self.course.course_id}.")
            
    def undo(self):
        if self.prerequisite_id in self.course.prerequisites:
            self.course.prerequisites.remove(self.prerequisite_id)
            print(f"Command undone: Removed prerequisite {self.prerequisite_id} from {self.course.course_id}.")

class ChangeCapacityCommand(Command):
    """Concrete command to change course capacity."""
    def __init__(self, course: Course, new_capacity: int):
        self.course = course
        self.new_capacity = new_capacity
        self.old_capacity = course.capacity
        
    def execute(self):
        self.course.capacity = self.new_capacity
        print(f"Command executed: Course {self.course.course_id} capacity changed to {self.new_capacity}.")
        
    def undo(self):
        self.course.capacity = self.old_capacity
        print(f"Command undone: Course {self.course.course_id} capacity reverted to {self.old_capacity}.")
