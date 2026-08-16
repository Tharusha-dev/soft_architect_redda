"""
Faculty Module implementation.
"""
from models.course import Course
from patterns.command import CourseChangeRequest
from patterns.state import GradeSubmission
from typing import Dict

class FacultyService:
    """Service handling faculty-specific business logic."""
    def submit_course_change_request(self, request: CourseChangeRequest, admin_service):
        """Submits a command-based course change request for admin approval."""
        print(f"FacultyService: Submitting course change request {request.request_id}...")
        admin_service.receive_course_change_request(request)
        
    def create_grade_submission(self, course_id: str, faculty_id: str) -> GradeSubmission:
        """Initiates a new grade submission process managed by the State pattern."""
        return GradeSubmission(course_id, faculty_id)
