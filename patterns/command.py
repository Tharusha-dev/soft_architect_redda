"""
Command Pattern implementation.
"""
from abc import ABC, abstractmethod
from typing import List
from collections import deque
from models.course import Course, CourseOffering, EnrollmentRepository, Schedule, Enrollment, ScheduleEntry, RequestStatus

# ---------------------------------------------------------
# Command A: Instructure Course-Change Requests
# ---------------------------------------------------------
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
    def __init__(self, course: Course, newDescription: str):
        self.course = course
        self.newDescription = newDescription
        self.oldDescription = course.description
        
    def execute(self):
        self.course.setDescription(self.newDescription)
        print(f"Command executed: Course {self.course.course_id} description updated.")
        
    def undo(self):
        self.course.setDescription(self.oldDescription)
        print(f"Command undone: Course {self.course.course_id} description reverted.")

class AddPrerequisiteCommand(Command):
    """Concrete command to add a course prerequisite."""
    def __init__(self, course: Course, prerequisite: Course):
        self.course = course
        self.prerequisite = prerequisite
        
    def execute(self):
        if self.prerequisite.course_id not in self.course.prerequisites:
            self.course.addPrerequisite(self.prerequisite)
            print(f"Command executed: Added prerequisite {self.prerequisite.course_id} to {self.course.course_id}.")
            
    def undo(self):
        if self.prerequisite.course_id in self.course.prerequisites:
            self.course.prerequisites.remove(self.prerequisite.course_id)
            print(f"Command undone: Removed prerequisite {self.prerequisite.course_id} from {self.course.course_id}.")

class ChangeCapacityCommand(Command):
    """Concrete command to change course capacity."""
    def __init__(self, course: Course, newCapacity: int):
        self.course = course
        self.newCapacity = newCapacity
        self.oldCapacity = course.capacity
        
    def execute(self):
        self.course.setCapacity(self.newCapacity)
        print(f"Command executed: Course {self.course.course_id} capacity changed to {self.newCapacity}.")
        
    def undo(self):
        self.course.setCapacity(self.oldCapacity)
        print(f"Command undone: Course {self.course.course_id} capacity reverted to {self.oldCapacity}.")

class CourseChangeRequest:
    """Invoker for Course-Change Requests."""
    def __init__(self, request_id: str, course_id: str, instructure_id: str, command: Command):
        self.request_id = request_id
        self.course_id = course_id
        self.instructure_id = instructure_id
        self.command = command
        self.status = RequestStatus.PENDING

    def approve(self):
        self.command.execute()
        self.status = RequestStatus.APPROVED
        
    def reject(self):
        self.status = RequestStatus.REJECTED


# ---------------------------------------------------------
# Command B: Compensable Enrolment Saga Steps
# ---------------------------------------------------------
class CompensableCommand(Command):
    @abstractmethod
    def compensate(self):
        pass

class ReserveSeatCommand(CompensableCommand):
    def __init__(self, offering: CourseOffering):
        self.offering = offering

    def execute(self):
        if not self.offering.reserveSeat():
            raise Exception("No seats available")
        print("Saga Step: reserved seat.")

    def compensate(self):
        self.offering.releaseSeat()
        print("Saga Compensation: released seat.")

    def undo(self):
        self.compensate()

class CreateEnrollmentCommand(CompensableCommand):
    def __init__(self, repository: EnrollmentRepository, enrollment: Enrollment):
        self.repository = repository
        self.enrollment = enrollment

    def execute(self):
        self.repository.save(self.enrollment)
        print("Saga Step: created enrolment record.")

    def compensate(self):
        self.repository.delete(self.enrollment)
        print("Saga Compensation: removed enrolment record.")

    def undo(self):
        self.compensate()

class UpdateScheduleCommand(CompensableCommand):
    def __init__(self, schedule: Schedule, entry: ScheduleEntry):
        self.schedule = schedule
        self.entry = entry

    def execute(self):
        self.schedule.addEntry(self.entry)
        print("Saga Step: added schedule entry.")

    def compensate(self):
        self.schedule.removeEntry(self.entry)
        print("Saga Compensation: removed schedule entry.")

    def undo(self):
        self.compensate()

class SagaOrchestrator:
    def __init__(self):
        self.steps: List[CompensableCommand] = []
        self.executed = deque()

    def run(self) -> bool:
        try:
            for step in self.steps:
                step.execute()
                self.executed.append(step)
            return True
        except Exception as e:
            print(f"Saga execution failed: {e}. Starting compensation.")
            while self.executed:
                cmd = self.executed.pop()
                cmd.compensate()
            return False
