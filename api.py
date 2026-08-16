"""
API Wrapper for NexusEnroll Core Business Logic
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.course import Course, CourseOffering, EnrollmentRepository, Schedule
from models.user import UserDetails
from patterns.factory import StudentCreator, FacultyCreator, AdministratorCreator
from patterns.command import ChangeCapacityCommand, CourseChangeRequest
from services.notification_service import NotificationService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from services.faculty_service import FacultyService
from services.admin_service import AdminService
from models.course import EnrollmentResult

app = Flask(__name__)
CORS(app)

# 1. Initialize Users
student_creator = StudentCreator()
faculty_creator = FacultyCreator()
admin_creator = AdministratorCreator()

s1 = student_creator.registerUser(UserDetails("20261011", "Alex Johnson", "alex@nexus.edu"))
s2 = student_creator.registerUser(UserDetails("20261012", "Maria Garcia", "maria@nexus.edu"))
s3 = student_creator.registerUser(UserDetails("20261013", "James Smith", "james@nexus.edu"))
s4 = student_creator.registerUser(UserDetails("20261014", "Linda Chen", "linda@nexus.edu"))

f1 = faculty_creator.registerUser(UserDetails("F105", "Prof. Johnson", "johnson@nexus.edu"))

# 2. Initialize Courses
# Mapping JS course ids to strings
courses_data = [
    Course("1", "SCS2301", "Data Structures and Algorithms", "Dr. Smith", 50, "Mon/Wed 10:00 AM - 12:00 PM"),
    Course("2", "SCS2303", "Software Architecture", "Prof. Johnson", 40, "Tue/Thu 1:00 PM - 3:00 PM"),
    Course("3", "SCS2305", "Database Management Systems", "Dr. Lee", 60, "Fri 9:00 AM - 12:00 PM"),
    Course("4", "SCS3201", "Machine Learning", "Dr. Adams", 30, "Mon/Wed 2:00 PM - 4:00 PM"),
    Course("5", "SCS1101", "Introduction to Programming", "Prof. Davis", 100, "Mon/Wed 8:00 AM - 10:00 AM")
]
courses_data[0].prerequisites = [5] # Using int to match frontend expectations
courses_data[1].prerequisites = ["SCS2101"] 
courses_data[3].prerequisites = [1]

s1.completed_courses = {5: "A", "SCS2101": "B"}
f1.teaching_courses = ["2"]
s1.enrolled_courses.append("1")

repository = EnrollmentRepository()
schedule = Schedule()

offerings = {}
for c in courses_data:
    offerings[c.course_id] = CourseOffering(c.course_id, c.capacity)
    
offerings["1"].enrolled_count = 48
offerings["2"].enrolled_count = 40
offerings["3"].enrolled_count = 15
offerings["4"].enrolled_count = 25
offerings["5"].enrolled_count = 95

notification_service = NotificationService()
event_publisher = notification_service.get_publisher()

facades = {}
for cid, offering in offerings.items():
    es = EnrollmentService(event_publisher, offering, repository, schedule)
    facades[cid] = es.get_facade()

class APIStudentService:
    def enroll_in_course(self, student_id: str, course_id: str):
        facade = facades.get(str(course_id))
        if not facade:
            return EnrollmentResult.FAILURE
        
        # Manually enforcing prerequisite and capacity checks for the API layer mapping
        course = next((c for c in courses_data if c.course_id == course_id), None)
        student = next((s for s in [s1, s2, s3, s4] if s.id == student_id), None)
        
        for prereq in course.prerequisites:
            if prereq not in student.completed_courses:
                return EnrollmentResult.FAILURE
                
        if offerings[course_id].enrolled_count >= course.capacity:
            return EnrollmentResult.FAILURE

        result = facade.enroll(student_id, str(course_id))
        if result == EnrollmentResult.SUCCESS:
            student.enrolled_courses.append(str(course_id))
        return result

    def drop_course(self, student_id: str, course_id: str):
        facade = facades.get(str(course_id))
        if facade:
            facade.drop(student_id, str(course_id))
            student = next((s for s in [s1, s2, s3, s4] if s.id == student_id), None)
            if str(course_id) in student.enrolled_courses:
                student.enrolled_courses.remove(str(course_id))

api_student_service = APIStudentService()

@app.route('/api/state', methods=['GET'])
def get_state():
    return jsonify({
        "courses": [
            {
                "id": int(c.course_id), 
                "code": c.name, 
                "title": c.description, 
                "instructor": c.instructor_id, 
                "capacity": c.capacity, 
                "enrolled": offerings[c.course_id].enrolled_count, 
                "schedule": c.schedule, 
                "prerequisites": c.prerequisites, 
                "credits": 3 
            } for c in courses_data
        ],
        "student": {
            "id": s1.id,
            "name": s1.name,
            "completedCourses": list(s1.completed_courses.keys()),
            "enrolledCourses": [int(c) for c in s1.enrolled_courses]
        },
        "faculty": {
            "id": f1.id,
            "name": f1.name,
            "taughtCourses": [int(c) for c in f1.teaching_courses]
        },
        "students": [
            {"id": s.id, "name": s.name, "grade": ""} for s in [s1, s2, s3, s4]
        ]
    })

@app.route('/api/enroll', methods=['POST'])
def enroll():
    data = request.json
    student_id = str(data.get('student_id'))
    course_id = str(data.get('course_id'))
    
    result = api_student_service.enroll_in_course(student_id, course_id)
    if result == EnrollmentResult.SUCCESS:
        return jsonify({"status": "success", "message": f"Successfully enrolled in course {course_id}"})
    return jsonify({"status": "error", "message": "Enrollment failed due to missing prerequisites or course is full."}), 400

@app.route('/api/drop', methods=['POST'])
def drop():
    data = request.json
    student_id = str(data.get('student_id'))
    course_id = str(data.get('course_id'))
    api_student_service.drop_course(student_id, course_id)
    return jsonify({"status": "success", "message": f"Successfully dropped course {course_id}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
