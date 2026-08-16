"""
State Pattern implementation.
As dictated by the System Design Report: The State Pattern is used to manage the 
lifecycle of a faculty grade submission. The concrete states are DraftState, 
PendingState, and SubmittedState.
"""
from abc import ABC, abstractmethod
from typing import Dict

class GradeState(ABC):
    """Abstract State class defining valid operations for a grade submission."""
    @abstractmethod
    def submit(self, submission: 'GradeSubmission'):
        pass

    @abstractmethod
    def approve(self, submission: 'GradeSubmission'):
        pass

    @abstractmethod
    def edit(self, submission: 'GradeSubmission', grades: Dict[str, str]):
        pass

class DraftState(GradeState):
    """Concrete State: Grades are being edited and drafted."""
    def submit(self, submission: 'GradeSubmission'):
        print(f"GradeState [Draft]: Submitting grades for {submission.course_id}. Moving to Pending State.")
        submission.set_state(PendingState())
        
    def approve(self, submission: 'GradeSubmission'):
        print("GradeState [Draft]: Cannot approve a draft. Must submit first.")
        
    def edit(self, submission: 'GradeSubmission', grades: Dict[str, str]):
        print("GradeState [Draft]: Editing draft grades.")
        submission.grades.update(grades)

class PendingState(GradeState):
    """Concrete State: Grades are submitted and awaiting admin approval."""
    def submit(self, submission: 'GradeSubmission'):
        print("GradeState [Pending]: Grades already submitted. Awaiting approval.")
        
    def approve(self, submission: 'GradeSubmission'):
        print(f"GradeState [Pending]: Approving grades for {submission.course_id}. Moving to Submitted State.")
        submission.set_state(SubmittedState())
        
    def edit(self, submission: 'GradeSubmission', grades: Dict[str, str]):
        print("GradeState [Pending]: Cannot edit while pending. Reverting to Draft State for edits.")
        submission.set_state(DraftState())
        submission.grades.update(grades)

class SubmittedState(GradeState):
    """Concrete State: Grades are finalized."""
    def submit(self, submission: 'GradeSubmission'):
        print("GradeState [Submitted]: Grades are already finalized.")
        
    def approve(self, submission: 'GradeSubmission'):
        print("GradeState [Submitted]: Grades are already approved.")
        
    def edit(self, submission: 'GradeSubmission', grades: Dict[str, str]):
        print("GradeState [Submitted]: Error - Cannot edit approved grades.")

class GradeSubmission:
    """The Context class that maintains a reference to the current GradeState."""
    def __init__(self, course_id: str, faculty_id: str):
        self.course_id = course_id
        self.faculty_id = faculty_id
        self.grades: Dict[str, str] = {} # student_id: grade
        self.state: GradeState = DraftState()
        
    def set_state(self, state: GradeState):
        """Transitions to a new state."""
        self.state = state
        
    def submit(self):
        self.state.submit(self)
        
    def approve(self):
        self.state.approve(self)
        
    def edit(self, grades: Dict[str, str]):
        self.state.edit(self, grades)
