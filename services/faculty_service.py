"""
Faculty Module implementation.
"""
from models.course import CourseChangeRequest, Course
from models.user import Student
from patterns.state import GradeSubmission
from typing import Dict

class FacultyService:
    """Service handling faculty-specific business logic."""
    def view_class_roster(self, faculty_id: str, course_id: str, courses_db: Dict[str, Course], students_db: Dict[str, Student]):
        """Views the roster for a given class."""
        course = courses_db.get(course_id)
        if not course or course.instructor_id != faculty_id:
            print("Access denied or course not found.")
            return
            
        print(f"\n--- Roster for {course.name} ---")
        for sid in course.enrolled_students:
            student = students_db.get(sid)
            print(f"{student.name} ({student.user_id}) - {student.email}")
        print("--------------------------------\n")
        
    def submit_course_change_request(self, request: CourseChangeRequest, admin_service):
        """Submits a command-based course change request for admin approval."""
        print(f"FacultyService: Submitting course change request {request.request_id}...")
        admin_service.receive_course_change_request(request)
        
    def create_grade_submission(self, course_id: str, faculty_id: str) -> GradeSubmission:
        """Initiates a new grade submission process managed by the State pattern."""
        return GradeSubmission(course_id, faculty_id)
