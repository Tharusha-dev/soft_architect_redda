"""
Administrator Module implementation.
"""
from models.course import CourseChangeRequest
from patterns.template_method import EnrollmentStatisticsReport, FacultyWorkloadReport, CoursePopularityReport
from typing import List

class AdminService:
    """Service handling administrator-specific business logic."""
    def __init__(self):
        self.pending_course_requests: List[CourseChangeRequest] = []
        
    def receive_course_change_request(self, request: CourseChangeRequest):
        """Receives a course change request from faculty."""
        self.pending_course_requests.append(request)
        print(f"AdminService: Received course change request {request.request_id}.")
        
    def approve_course_change_request(self, request_id: str):
        """Approves and executes a pending course change request."""
        for req in self.pending_course_requests:
            if req.request_id == request_id:
                print(f"AdminService: Approving request {request_id}...")
                # Executes the encapsulated command
                req.command.execute()
                req.status = "Approved"
                self.pending_course_requests.remove(req)
                return
        print("AdminService: Request not found.")
        
    def generate_enrollment_statistics(self):
        """Generates enrollment report using Template Method."""
        report = EnrollmentStatisticsReport()
        report.generate_report()
        
    def generate_faculty_workload(self):
        """Generates faculty workload report using Template Method."""
        report = FacultyWorkloadReport()
        report.generate_report()
        
    def generate_course_popularity(self):
        """Generates course popularity report using Template Method."""
        report = CoursePopularityReport()
        report.generate_report()
