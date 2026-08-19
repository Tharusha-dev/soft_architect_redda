"""
Instructure Module implementation.
"""
from models.course import Course
from patterns.command import CourseChangeRequest
from patterns.state import GradeSubmission
from typing import Dict

class InstructureService:
    """Service handling instructure-specific business logic."""
    def submit_course_change_request(self, request: CourseChangeRequest, admin_service):
        """Submits a command-based course change request for admin approval."""
        print(f"InstructureService: Submitting course change request {request.request_id}...")
        admin_service.receive_course_change_request(request)
        
    def create_grade_submission(self, course_id: str, instructure_id: str) -> GradeSubmission:
        """Initiates a new grade submission process managed by the State pattern."""
        return GradeSubmission(course_id, instructure_id)
