"""
State Pattern implementation.
"""
from abc import ABC, abstractmethod
from typing import List

class GradeRecord:
    def __init__(self, student_id: str, grade: str):
        self.student_id = student_id
        self.grade = grade

class GradeState(ABC):
    """Abstract State class defining valid operations for a grade submission."""
    @abstractmethod
    def submit(self, ctx: 'GradeSubmission'):
        pass

    @abstractmethod
    def approve(self, ctx: 'GradeSubmission'):
        pass

    @abstractmethod
    def edit(self, ctx: 'GradeSubmission'):
        pass

class DraftState(GradeState):
    """Concrete State: Grades are being edited and drafted."""
    def submit(self, ctx: 'GradeSubmission'):
        print(f"GradeState [Draft]: Submitting grades. Moving to Pending State.")
        ctx.setState(PendingState())
        
    def approve(self, ctx: 'GradeSubmission'):
        print("GradeState [Draft]: Cannot approve a draft. Must submit first.")
        
    def edit(self, ctx: 'GradeSubmission'):
        print("GradeState [Draft]: Editing draft grades. (allowed)")

class PendingState(GradeState):
    """Concrete State: Grades are submitted and awaiting admin approval."""
    def submit(self, ctx: 'GradeSubmission'):
        print("GradeState [Pending]: Grades already submitted. (already pending)")
        
    def approve(self, ctx: 'GradeSubmission'):
        print(f"GradeState [Pending]: Approving grades. Moving to Submitted State.")
        ctx.setState(SubmittedState())
        
    def edit(self, ctx: 'GradeSubmission'):
        print("GradeState [Pending]: Cannot edit while pending. (locked while pending)")

class SubmittedState(GradeState):
    """Concrete State: Grades are finalized."""
    def submit(self, ctx: 'GradeSubmission'):
        print("GradeState [Submitted]: Grades are already finalized. (final state)")
        
    def approve(self, ctx: 'GradeSubmission'):
        print("GradeState [Submitted]: Grades are already approved. (final state)")
        
    def edit(self, ctx: 'GradeSubmission'):
        print("GradeState [Submitted]: Error - Cannot edit approved grades. (final state)")

class GradeSubmission:
    """The Context class that maintains a reference to the current GradeState."""
    def __init__(self, course_id: str, faculty_id: str):
        self.course_id = course_id
        self.faculty_id = faculty_id
        self.grades: List[GradeRecord] = []
        self.state: GradeState = DraftState()
        
    def setState(self, s: GradeState):
        """Transitions to a new state."""
        self.state = s
        
    def submit(self):
        self.state.submit(self)
        
    def approve(self):
        self.state.approve(self)
        
    def edit(self):
        self.state.edit(self)
