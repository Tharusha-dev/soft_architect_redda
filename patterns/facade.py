"""
Facade Pattern implementation.
As dictated by the System Design Report: The Facade Pattern is used within the 
Enrollment Service to provide a simplified interface to the different components 
involved in the enrolment process.
"""
from patterns.chain_of_responsibility import ValidationChain
from patterns.observer import EventPublisher
from models.user import Student
from models.course import Course
from typing import Dict

class EnrollmentFacade:
    """Coordinates validation, persistence, and event publication."""
    def __init__(self, event_publisher: EventPublisher, courses_db: Dict[str, Course], students_db: Dict[str, Student]):
        self.validator = ValidationChain()
        self.event_publisher = event_publisher
        self.courses_db = courses_db
        self.students_db = students_db
        
    def enroll(self, student_id: str, course_id: str) -> bool:
        """Facade method to handle the enrollment workflow."""
        student = self.students_db.get(student_id)
        course = self.courses_db.get(course_id)
        
        if not student or not course:
            print("Error: Student or Course not found.")
            return False
            
        print(f"Facade: Attempting to enroll {student.name} in {course.name}...")
        
        # 1. Coordinate Validation
        if not self.validator.validate(student, course):
            print("Facade: Enrollment failed due to validation errors.")
            return False
            
        # 2. Coordinate Persistence / Transactional State Changes
        try:
            course.enrolled_students.append(student_id)
            student.enrolled_courses.append(course_id)
            print(f"Facade: Enrollment successful for {student.name} in {course.name}.")
            
            # 3. Coordinate Event Publication
            self.event_publisher.publish("ENROLLMENT_SUCCESS", {"student_id": student_id, "course_id": course_id})
            return True
        except Exception as e:
            print(f"Facade: Transaction failed: {e}")
            self.event_publisher.publish("SYSTEM_ERROR", {"message": f"Enrollment transaction failed: {e}"})
            return False

    def drop(self, student_id: str, course_id: str) -> bool:
        """Facade method to handle the course dropping workflow."""
        student = self.students_db.get(student_id)
        course = self.courses_db.get(course_id)
        
        if not student or not course:
            return False
            
        if course_id in student.enrolled_courses:
            # Transactional logic
            student.enrolled_courses.remove(course_id)
            if student_id in course.enrolled_students:
                course.enrolled_students.remove(student_id)
            print(f"Facade: Drop successful. {student.name} dropped {course.name}.")
            
            # Event publication
            self.event_publisher.publish("COURSE_DROPPED", {"student_id": student_id, "course_id": course_id})
            return True
        else:
            print("Facade: Student is not enrolled in this course.")
            return False
