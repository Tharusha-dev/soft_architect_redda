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
        self.courses = []
        self.users = []
        self.programs = []
        
    def create_course(self, course):
        self.courses.append(course)
        print(f"AdminService: Course {course.course_id} created.")
        
    def delete_course(self, course_id: str):
        self.courses = [c for c in self.courses if c.course_id != course_id]
        print(f"AdminService: Course {course_id} deleted.")
        
    def add_user(self, user):
        self.users.append(user)
        print(f"AdminService: User {user.name} added.")
        
    def deactivate_user(self, user_id: str):
        for u in self.users:
            if u.id == user_id:
                if hasattr(u, 'deactivate'):
                    u.deactivate()
                    print(f"AdminService: User {user_id} deactivated.")
                    
    def define_program(self, program):
        self.programs.append(program)
        print(f"AdminService: Degree Program {program.id} defined.")
        
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
