"""
API Wrapper for NexusEnroll Core Business Logic
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from models.course import Course, CourseOffering, EnrollmentRepository, Schedule
from models.user import UserDetails
from patterns.factory import StudentCreator, InstructureCreator, AdministratorCreator
from patterns.command import ChangeCapacityCommand, CourseChangeRequest
from services.notification_service import NotificationService
from services.enrollment_service import EnrollmentService
from services.student_service import StudentService
from services.instructure_service import InstructureService
from services.admin_service import AdminService
from patterns.facade import EnrollmentFacade
from models.course import EnrollmentResult

app = Flask(__name__)
CORS(app)

# 1. Initialize Users
student_creator = StudentCreator()
instructure_creator = InstructureCreator()
admin_creator = AdministratorCreator()

s1 = student_creator.registerUser(UserDetails("20261011", "Alex Johnson", "alex@nexus.edu"))
s2 = student_creator.registerUser(UserDetails("20261012", "Maria Garcia", "maria@nexus.edu"))
s3 = student_creator.registerUser(UserDetails("20261013", "James Smith", "james@nexus.edu"))
s4 = student_creator.registerUser(UserDetails("20261014", "Linda Chen", "linda@nexus.edu"))

f1 = instructure_creator.registerUser(UserDetails("F105", "Prof. Johnson", "johnson@nexus.edu"))

# 2. Initialize Courses
courses_data = [
    Course("1", "SCS2301", "Data Structures and Algorithms", "Dr. Smith", 50, "Mon/Wed 10:00 AM - 12:00 PM"),
    Course("2", "SCS2303", "Software Architecture", "Prof. Johnson", 40, "Tue/Thu 1:00 PM - 3:00 PM"),
    Course("3", "SCS2305", "Database Management Systems", "Dr. Lee", 60, "Fri 9:00 AM - 12:00 PM"),
    Course("4", "SCS3201", "Machine Learning", "Dr. Adams", 30, "Mon/Wed 2:00 PM - 4:00 PM"),
    Course("5", "SCS1101", "Introduction to Programming", "Prof. Davis", 100, "Mon/Wed 8:00 AM - 10:00 AM")
]
courses_data[0].prerequisites = ["5"]
courses_data[1].prerequisites = ["1"] 
courses_data[3].prerequisites = ["1"]

s1.completed_courses = {"5": "A", "1": "B"}
f1.teaching_courses = ["2"]
s1.enrolled_courses.append("3")

repository = EnrollmentRepository()
schedule = Schedule()

offerings = {}
for c in courses_data:
    offerings[c.course_id] = CourseOffering(c.course_id, c.capacity)
    
offerings["1"].enrolled_count = 48
offerings["2"].enrolled_count = 38
offerings["3"].enrolled_count = 15
offerings["4"].enrolled_count = 25
offerings["5"].enrolled_count = 95

notification_service = NotificationService()
event_publisher = notification_service.get_publisher()

notifications_db = []
class APINotificationObserver:
    def update(self, event):
        notifications_db.insert(0, {"type": event.type, "payload": event.payload, "timestamp": "Just now"})

event_publisher.subscribe(APINotificationObserver())

@app.route('/api/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    user_notifs = [n for n in notifications_db if str(n['payload'].get('student_id')) == str(user_id) or str(n['payload'].get('instructure_id')) == str(user_id)]
    return jsonify(user_notifs)



class DummyCourseRepo:
    def get(self, cid):
        return next((c for c in courses_data if c.course_id == str(cid)), None)

class DummyUserRepo:
    def get(self, uid):
        return next((s for s in [s1, s2, s3, s4, f1] if s.id == str(uid)), None)

course_repo = DummyCourseRepo()
user_repo = DummyUserRepo()

facades = {}
for cid, offering in offerings.items():
    facade = EnrollmentFacade(event_publisher, offering, repository, schedule, course_repo, user_repo, offerings)
    facades[cid] = facade


admin_service = AdminService()
instructure_service = InstructureService()

# Populate Admin Service Memory
for u in [s1, s2, s3, s4, f1]:
    admin_service.add_user(u)
for c in courses_data:
    admin_service.create_course(c)
from models.course import DegreeProgram
admin_service.define_program(DegreeProgram("CS-BS", "BSc Computer Science", 120, []))


class APIStudentService:
    def enroll_in_course(self, student_id: str, course_id: str):
        facade = facades.get(str(course_id))
        if not facade:
            return EnrollmentResult.FAILURE
        
        course = next((c for c in courses_data if c.course_id == course_id), None)
        student = next((s for s in [s1, s2, s3, s4] if s.id == student_id), None)
        
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
    def get_course_code(cid):
        c = next((c for c in courses_data if str(c.course_id) == str(cid)), None)
        return c.name if c else str(cid)

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
            "completedCourses": [{"id": get_course_code(k), "grade": v} for k, v in s1.completed_courses.items()],
            "enrolledCourses": [int(c) for c in s1.enrolled_courses],
            "waitlistedCourses": [int(c.course_id) for c in courses_data if s1.id in offerings[c.course_id].waitlist]
        },
        "instructure": {
            "id": f1.id,
            "name": f1.name,
            "taughtCourses": [int(c) for c in f1.teaching_courses]
        },
        "students": [
            {"id": s.id, "name": s.name, "completedCourses": {get_course_code(k): v for k, v in s.completed_courses.items()}} for s in [s1, s2, s3, s4]
        ],
        "admin": {
            "courses": [{"id": c.course_id, "name": c.name} for c in admin_service.courses],
            "users": [{"id": u.id, "name": u._name, "active": u.is_active} for u in admin_service.users],
            "programs": [{"id": p.id, "name": p.name} for p in admin_service.programs],
            "pending_requests": [
                {"id": req.request_id, "course_id": req.course_id} 
                for req in admin_service.pending_course_requests
            ],
            "pending_grades": [
                {"course_id": gs.course_id, "instructure_id": gs.instructure_id, "student_id": getattr(gs, 'student_id', None), "grade": getattr(gs, 'grade', None)}
                for gs in getattr(admin_service, 'pending_grades', [])
            ]
        }
    })

@app.route('/api/enroll', methods=['POST'])
def enroll():
    data = request.json
    result = api_student_service.enroll_in_course(str(data.get('student_id')), str(data.get('course_id')))
    if result == EnrollmentResult.SUCCESS:
        return jsonify({"status": "success", "message": f"Successfully enrolled in course {data.get('course_id')}"})
    return jsonify({"status": "error", "message": "Enrollment failed due to missing prerequisites or course is full."}), 400

@app.route('/api/drop', methods=['POST'])
def drop():
    data = request.json
    api_student_service.drop_course(str(data.get('student_id')), str(data.get('course_id')))
    return jsonify({"status": "success", "message": f"Successfully dropped course {data.get('course_id')}"})

@app.route('/api/instructure/grades/submit', methods=['POST'])
def submit_grades():
    data = request.json
    course_id = str(data.get('course_id'))
    instructure_id = str(data.get('instructure_id'))
    student_id = str(data.get('student_id'))
    grade = data.get('grade')
    
    grade_sub = instructure_service.create_grade_submission(course_id, instructure_id)
    grade_sub.edit()
    grade_sub.submit() # transitions to pending
    grade_sub.student_id = student_id
    grade_sub.grade = grade
    
    if not hasattr(admin_service, 'pending_grades'):
        admin_service.pending_grades = []
    # Avoid duplicates for the same student
    admin_service.pending_grades = [g for g in admin_service.pending_grades if not (g.course_id == course_id and getattr(g, 'student_id', None) == student_id)]
    admin_service.pending_grades.append(grade_sub)
    
    return jsonify({"status": "success", "message": f"Grade {grade} for {student_id} submitted (State Pattern: Pending)."})

@app.route('/api/instructure/change-capacity', methods=['POST'])
def change_capacity():
    data = request.json
    course_id = str(data.get('course_id'))
    instructure_id = str(data.get('instructure_id'))
    new_capacity = int(data.get('capacity', 0))
    
    course = next((c for c in courses_data if c.course_id == course_id), None)
    if not course: return jsonify({"error": "Course not found"}), 404
    
    change_cmd = ChangeCapacityCommand(course, new_capacity)
    import uuid
    req_id = str(uuid.uuid4())[:8]
    req = CourseChangeRequest(req_id, course_id, instructure_id, change_cmd)
    
    instructure_service.submit_course_change_request(req, admin_service)
    return jsonify({"status": "success", "message": f"Command Pattern: Change request {req_id} sent to Admin."})

@app.route('/api/admin/approve-request', methods=['POST'])
def approve_request():
    req_id = request.json.get('request_id')
    admin_service.approve_course_change_request(req_id)
    # Also update the CourseOffering object so the API reflects the change
    for course in courses_data:
        if course.course_id in offerings:
            offerings[course.course_id].capacity = course.capacity
    return jsonify({"status": "success", "message": f"Command Pattern: Request {req_id} executed and approved."})

@app.route('/api/admin/reports', methods=['GET'])
def get_reports():
    from patterns.template_method import EnrollmentStatisticsReport, InstructureWorkloadReport, CoursePopularityReport
    stats = EnrollmentStatisticsReport().generateReport().content
    workload = InstructureWorkloadReport().generateReport().content
    popularity = CoursePopularityReport().generateReport().content
    
    return jsonify({
        "stats": stats,
        "workload": workload,
        "popularity": popularity
    })

@app.route('/api/admin/approve-grades', methods=['POST'])
def approve_grades():
    data = request.json
    course_id = str(data.get('course_id'))
    student_id = str(data.get('student_id'))
    if hasattr(admin_service, 'pending_grades'):
        for gs in admin_service.pending_grades:
            if gs.course_id == course_id and getattr(gs, 'student_id', None) == student_id:
                gs.approve() # State Pattern transition
                admin_service.pending_grades.remove(gs)
                
                student = next((s for s in [s1, s2, s3, s4] if s.id == student_id), None)
                if student:
                    student.completed_courses[str(course_id)] = getattr(gs, 'grade', 'P')

                return jsonify({"status": "success", "message": f"State Pattern: Grades for course {course_id} approved."})
    return jsonify({"status": "error", "message": "No pending grades found."}), 404

@app.route('/api/admin/courses', methods=['POST'])
def create_course():
    data = request.json
    new_course = Course(
        str(data.get('code')), data.get('code'), data.get('title'), 
        data.get('instructor'), int(data.get('capacity', 50)), "TBD"
    )
    courses_data.append(new_course)
    offerings[new_course.course_id] = CourseOffering(new_course.course_id, new_course.capacity)
    offerings[new_course.course_id].enrolled_count = 0
    facades[new_course.course_id] = EnrollmentService(event_publisher, offerings[new_course.course_id], repository, schedule).get_facade()
    return jsonify({"status": "success", "message": "Course created (Standard CRUD)."})

@app.route('/api/admin/courses/edit', methods=['PUT'])
def edit_course():
    data = request.json
    course_id = str(data.get('id'))
    course = next((c for c in courses_data if c.course_id == course_id), None)
    if course:
        course.name = data.get('code')
        course.description = data.get('title')
        return jsonify({"status": "success", "message": "Course edited (Standard CRUD)."})
    return jsonify({"status": "error", "message": "Course not found."}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

@app.route('/api/admin/courses', methods=['POST'])
def add_course():
    data = request.json
    c = Course(str(data['id']), data['name'], data['desc'], data['instructor'], int(data['capacity']), data['schedule'])
    admin_service.create_course(c)
    courses_data.append(c)
    offerings[c.course_id] = CourseOffering(c.course_id, c.capacity)
    facades[c.course_id] = EnrollmentFacade(event_publisher, offerings[c.course_id], repository, schedule, course_repo, user_repo, offerings)
    return jsonify({"status": "success"})

@app.route('/api/admin/users/deactivate', methods=['POST'])
def deactivate_user_api():
    uid = request.json['id']
    admin_service.deactivate_user(str(uid))
    return jsonify({"status": "success"})

@app.route('/api/admin/programs', methods=['POST'])
def add_program():
    data = request.json
    from models.course import DegreeProgram
    admin_service.define_program(DegreeProgram(data['id'], data['name'], 120, []))
    return jsonify({"status": "success"})

@app.route('/api/instructure/change-desc', methods=['POST'])
def change_desc():
    data = request.json
    from patterns.command import UpdateDescriptionCommand, CourseChangeRequest
    import uuid
    course = next((c for c in courses_data if c.course_id == str(data['course_id'])), None)
    req = CourseChangeRequest(str(uuid.uuid4())[:8], course.course_id, data['instructure_id'], UpdateDescriptionCommand(course, data['desc']))
    instructure_service.submit_course_change_request(req, admin_service)
    return jsonify({"status": "success"})

@app.route('/api/instructure/change-prereq', methods=['POST'])
def change_prereq():
    data = request.json
    from patterns.command import AddPrerequisiteCommand, CourseChangeRequest
    import uuid
    course = next((c for c in courses_data if c.course_id == str(data['course_id'])), None)
    prereq_course = next((c for c in courses_data if c.course_id == str(data['prereq_id'])), None)
    if prereq_course:
        req = CourseChangeRequest(str(uuid.uuid4())[:8], course.course_id, data['instructure_id'], AddPrerequisiteCommand(course, prereq_course))
        instructure_service.submit_course_change_request(req, admin_service)
    return jsonify({"status": "success"})

@app.route('/api/admin/users/add', methods=['POST'])
def add_user_api():
    data = request.json
    role = data.get('role', 'student')
    if role == 'student':
        u = student_creator.registerUser(UserDetails(data['id'], data['name'], data['id']+"@nexus.edu"))
    else:
        u = instructure_creator.registerUser(UserDetails(data['id'], data['name'], data['id']+"@nexus.edu"))
    admin_service.add_user(u)
    return jsonify({"status": "success"})

@app.route('/api/admin/users/edit', methods=['POST'])
def edit_user_api():
    data = request.json
    uid = data['id']
    for u in admin_service.users:
        if u.id == uid:
            u._name = data['name']
    return jsonify({"status": "success"})
    
@app.route('/api/admin/courses/edit', methods=['POST'])
def edit_course_api():
    data = request.json
    cid = data['id']
    for c in admin_service.courses:
        if c.course_id == cid:
            c.name = data['name']
            c.capacity = int(data['capacity'])
    return jsonify({"status": "success"})
