"""
Administrator Module implementation.
"""
from patterns.command import CourseChangeRequest
from patterns.template_method import EnrollmentStatisticsReport, InstructureWorkloadReport, CoursePopularityReport
from typing import List

class AdminService:
    """Service handling administrator-specific business logic."""
    def __init__(self):
        self.pending_course_requests: List[CourseChangeRequest] = []
        
    def receive_course_change_request(self, request: CourseChangeRequest):
        """Receives a course change request from instructure."""
        self.pending_course_requests.append(request)
        print(f"AdminService: Received course change request {request.request_id}.")
        
    def approve_course_change_request(self, request_id: str):
        """Approves and executes a pending course change request."""
        for req in self.pending_course_requests:
            if req.request_id == request_id:
                print(f"AdminService: Approving request {request_id}...")
                req.approve()
                self.pending_course_requests.remove(req)
                return
        print("AdminService: Request not found.")
        
    def generate_reports(self):
        """Generates structured reports."""
        print(EnrollmentStatisticsReport().generateReport().content)
        print(CoursePopularityReport().generateReport().content)
