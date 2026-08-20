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

import json

# 1. Initialize Users and Courses from seed_data.json
student_creator = StudentCreator()
instructure_creator = InstructureCreator()
admin_creator = AdministratorCreator()

all_users = []
courses_data = []
offerings = {}
programs_data = []

with open('seed_data.json', 'r') as f:
    seed_data = json.load(f)

programs_data = seed_data.get('programs', [])

for u_data in seed_data.get('users', []):
    if u_data['role'] == 'student':
        u = student_creator.registerUser(UserDetails(u_data['id'], u_data['name'], u_data['email']))
        u.completed_courses = u_data.get('completed_courses', {})
        u.role = 'student'
        all_users.append(u)
    elif u_data['role'] == 'instructure':
        u = instructure_creator.registerUser(UserDetails(u_data['id'], u_data['name'], u_data['email']))
        u.teaching_courses = u_data.get('teaching_courses', [])
        u.role = 'instructure'
        all_users.append(u)
    else:
        u = admin_creator.registerUser(UserDetails(u_data['id'], u_data['name'], u_data['email']))
        u.role = 'admin'
        all_users.append(u)

for c_data in seed_data.get('courses', []):
    c = Course(c_data['course_id'], c_data['name'], c_data['description'], c_data['instructor_id'], c_data['capacity'], c_data['schedule'], c_data.get('department', ''), c_data.get('days', ''), c_data.get('start_time', ''), c_data.get('end_time', ''))
    c.prerequisites = c_data.get('prerequisites', [])
    courses_data.append(c)
    offerings[c.course_id] = CourseOffering(c.course_id, c.capacity)
    offerings[c.course_id].enrolled_count = 0

repository = EnrollmentRepository()
schedule = Schedule()

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
        return next((s for s in all_users if s.id == str(uid)), None)

course_repo = DummyCourseRepo()
user_repo = DummyUserRepo()

facades = {}
for cid, offering in offerings.items():
    facade = EnrollmentFacade(event_publisher, offering, repository, schedule, course_repo, user_repo, offerings)
    facades[cid] = facade


admin_service = AdminService()
instructure_service = InstructureService()

# Populate Admin Service Memory
for u in all_users:
    admin_service.add_user(u)
for c in courses_data:
    admin_service.create_course(c)
from models.course import DegreeProgram
for p_data in seed_data.get('programs', []):
    admin_service.define_program(DegreeProgram(p_data['id'], p_data['name'], p_data['required_credits'], p_data.get('required_courses', [])))


class APIStudentService:
    def enroll_in_course(self, student_id: str, course_id: str):
        facade = facades.get(str(course_id))
        if not facade:
            return EnrollmentResult.FAILURE, "Course not found."
        
        course = next((c for c in courses_data if c.course_id == course_id), None)
        student = next((s for s in [u for u in all_users if hasattr(u, "completed_courses")] if s.id == student_id), None)
        
        result, msg = facade.enroll(student_id, str(course_id))
        if result == EnrollmentResult.SUCCESS:
            student.enrolled_courses.append(str(course_id))
        return result, msg

    def drop_course(self, student_id: str, course_id: str):
        facade = facades.get(str(course_id))
        if facade:
            facade.drop(student_id, str(course_id))
            student = next((s for s in [u for u in all_users if hasattr(u, "completed_courses")] if s.id == student_id), None)
            if str(course_id) in student.enrolled_courses:
                student.enrolled_courses.remove(str(course_id))

    def waitlist_course(self, student_id: str, course_id: str):
        facade = facades.get(str(course_id))
        if not facade:
            return EnrollmentResult.FAILURE, "Course not found."
        return facade.waitlist(student_id, str(course_id))

api_student_service = APIStudentService()

@app.route('/api/state', methods=['GET'])
def get_state():
    def get_course_code(cid):
        c = next((c for c in courses_data if str(c.course_id) == str(cid)), None)
        return c.name if c else str(cid)

    uid = request.args.get('uid')
    current_user = next((u for u in all_users if u.id == uid), None)
    
    student_data = None
    if current_user and hasattr(current_user, 'completed_courses'):
        student_data = {
            "id": current_user.id,
            "name": current_user._name,
            "completedCourses": [{"id": get_course_code(k), "grade": v} for k, v in getattr(current_user, 'completed_courses', {}).items()],
            "enrolledCourses": getattr(current_user, 'enrolled_courses', []),
            "waitlistedCourses": [c.course_id for c in courses_data if current_user.id in offerings[c.course_id].waitlist],
            "program_id": getattr(current_user, 'program_id', 'BSc_CS')
        }
        
    instructure_data = None
    if current_user and hasattr(current_user, 'teaching_courses'):
        # Dynamically compute courses taught by this instructor
        taught_course_ids = [c.course_id for c in courses_data if str(c.instructor_id) == str(current_user.id)]
        instructure_data = {
            "id": current_user.id,
            "name": current_user._name,
            "taughtCourses": taught_course_ids
        }

    students_list = [
        {"id": s.id, "name": s._name, "enrolledCourses": getattr(s, 'enrolled_courses', []), "completedCourses": {get_course_code(k): v for k, v in getattr(s, 'completed_courses', {}).items()}} for s in all_users if hasattr(s, 'completed_courses')
    ]

    return jsonify({
        "courses": [
            {
                "id": c.course_id, 
                "code": c.name, 
                "title": c.description, 
                "instructor": c.instructor_id, 
                "capacity": c.capacity, 
                "enrolled": offerings[c.course_id].enrolled_count, 
                "schedule": c.schedule, 
                "prerequisites": c.prerequisites, 
                "credits": getattr(c, 'credits', 3),
                "department": getattr(c, 'department', ''),
                "days": getattr(c, 'days', ''),
                "start_time": getattr(c, 'start_time', ''),
                "end_time": getattr(c, 'end_time', ''),
                "schedule_history": getattr(c, 'schedule_history', [])
            } for c in courses_data
        ],
        "student": student_data,
        "instructure": instructure_data,
        "students": students_list,
        "programs": programs_data,
        "admin": {
            "courses": [{"id": c.course_id, "name": c.name, "department": getattr(c, 'department', ''), "instructor": c.instructor_id, "capacity": c.capacity, "enrolled_count": offerings[c.course_id].enrolled_count if c.course_id in offerings else 0} for c in admin_service.courses],
            "users": [{"id": u.id, "name": u._name, "email": getattr(u, '_email', ''), "active": u.is_active, "role": getattr(u, 'role', 'unknown')} for u in admin_service.users],
            "programs": [{"id": p.id, "name": p.name, "required_credits": getattr(p, 'required_credits', 120), "required_courses": getattr(p, 'required_courses', [])} for p in admin_service.programs],
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

@app.route('/api/courses/search', methods=['GET'])
def search_courses():
    query = request.args.get('q', '').lower()
    dept = request.args.get('dept', '').lower()
    instructor = request.args.get('instructor', '').lower()
    
    results = []
    for c in courses_data:
        # Check department
        if dept and dept not in getattr(c, 'department', '').lower():
            continue
            
        # Check instructor (either name or ID)
        if instructor and instructor not in c.instructor_id.lower():
            inst_obj = next((u for u in all_users if u.id == c.instructor_id), None)
            if not inst_obj or instructor not in inst_obj._name.lower():
                continue
                
        # Check keyword query (against course code, title, description)
        if query:
            if query not in c.course_id.lower() and query not in c.name.lower() and query not in getattr(c, 'description', '').lower():
                continue
                
        # Course matches all filters!
        results.append({
            "id": c.course_id, 
            "code": c.name, 
            "title": c.description, 
            "instructor": c.instructor_id, 
            "capacity": c.capacity, 
            "enrolled": offerings[c.course_id].enrolled_count if c.course_id in offerings else 0, 
            "schedule": c.schedule, 
            "prerequisites": getattr(c, 'prerequisites', []), 
            "credits": getattr(c, 'credits', 3),
            "department": getattr(c, 'department', ''),
            "days": getattr(c, 'days', ''),
            "start_time": getattr(c, 'start_time', ''),
            "end_time": getattr(c, 'end_time', '')
        })
        
    return jsonify({"status": "success", "courses": results})

@app.route('/api/enroll', methods=['POST'])
def enroll():
    data = request.json
    result, msg = api_student_service.enroll_in_course(str(data.get('student_id')), str(data.get('course_id')))
    if result == EnrollmentResult.SUCCESS:
        return jsonify({"status": "success", "message": f"Successfully enrolled in course {data.get('course_id')}"})
    return jsonify({"status": "error", "message": msg}), 400

@app.route('/api/drop', methods=['POST'])
def drop():
    data = request.json
    api_student_service.drop_course(str(data.get('student_id')), str(data.get('course_id')))
    return jsonify({"status": "success", "message": f"Successfully dropped course {data.get('course_id')}"})

@app.route('/api/waitlist', methods=['POST'])
def waitlist():
    data = request.json
    result, msg = api_student_service.waitlist_course(str(data.get('student_id')), str(data.get('course_id')))
    if result.name == 'SUCCESS':
        return jsonify({"status": "success", "message": f"Successfully joined waitlist for course {data.get('course_id')}"})
    return jsonify({"status": "error", "message": msg}), 400

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

@app.route('/api/instructure/grades/submit_batch', methods=['POST'])
def submit_grades_batch():
    data = request.json
    course_id = str(data.get('course_id'))
    instructure_id = str(data.get('instructure_id'))
    grades = data.get('grades', [])
    
    valid_grades = ['A', 'B', 'C', 'D', 'F']
    processed = 0
    errors = []
    
    if not hasattr(admin_service, 'pending_grades'):
        admin_service.pending_grades = []
        
    for g_item in grades:
        student_id = str(g_item.get('student_id'))
        grade = g_item.get('grade')
        
        if grade not in valid_grades:
            errors.append(f"Invalid grade '{grade}' for student {student_id}")
            continue
            
        grade_sub = instructure_service.create_grade_submission(course_id, instructure_id)
        grade_sub.edit()
        grade_sub.submit()
        grade_sub.student_id = student_id
        grade_sub.grade = grade
        
        admin_service.pending_grades = [g for g in admin_service.pending_grades if not (g.course_id == course_id and getattr(g, 'student_id', None) == student_id)]
        admin_service.pending_grades.append(grade_sub)
        processed += 1
        
    msg = f"Processed {processed} grades."
    if errors:
        msg += f" Encountered {len(errors)} errors."
        return jsonify({"status": "warning", "message": msg, "errors": errors})
    return jsonify({"status": "success", "message": msg})

@app.route('/api/instructure/change-capacity', methods=['POST'])
def change_capacity():
    data = request.json
    course_id = str(data.get('course_id'))
    instructure_id = str(data.get('instructure_id'))
    new_capacity = int(data['capacity'])
    
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
    stats = EnrollmentStatisticsReport(courses_data, offerings).generateReport().content
    workload = InstructureWorkloadReport(courses_data, all_users).generateReport().content
    popularity = CoursePopularityReport(courses_data, offerings).generateReport().content
    
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
                
                student = next((s for s in [u for u in all_users if hasattr(u, "completed_courses")] if s.id == student_id), None)
                if student:
                    student.completed_courses[str(course_id)] = getattr(gs, 'grade', 'P')

                return jsonify({"status": "success", "message": f"State Pattern: Grades for course {course_id} approved."})
    return jsonify({"status": "error", "message": "No pending grades found."}), 404

@app.route('/api/admin/courses/edit', methods=['PUT', 'POST'])
def edit_course():
    data = request.json
    course_id = str(data.get('id'))
    course = next((c for c in courses_data if c.course_id == course_id), None)
    if course:
        if 'code' in data: course.name = data['code']
        if 'name' in data: course.name = data['name']
        if 'title' in data: course.description = data['title']
        if 'desc' in data: course.description = data['desc']
        if 'department' in data: course.department = data['department']
        if 'instructor' in data: course.instructor_id = data['instructor']
        if 'capacity' in data: 
            course.capacity = int(data['capacity'])
            if course_id in offerings: offerings[course_id].capacity = course.capacity
        if 'days' in data: course.days = data['days']
        if 'start_time' in data: course.start_time = data['start_time']
        if 'end_time' in data: course.end_time = data['end_time']
        return jsonify({"status": "success", "message": "Course edited (Standard CRUD)."})
    return jsonify({"status": "error", "message": "Course not found."}), 404


@app.route('/api/admin/courses', methods=['POST'])
def add_course():
    data = request.json
    course_id = str(data.get('id', data.get('code')))
    course_name = data.get('name', data.get('code', ''))
    course_desc = data.get('desc', data.get('title', ''))
    course_inst = data.get('instructor', 'Staff')
    course_cap = int(data.get('capacity', 0))
    
    c = Course(course_id, course_name, course_desc, course_inst, course_cap, data.get('schedule', 'TBD'), data.get('department', ''), data.get('days', ''), data.get('start_time', ''), data.get('end_time', ''))
    if 'prerequisites' in data and data['prerequisites']:
        for p in data['prerequisites'].split(','):
            pc = next((cx for cx in courses_data if cx.course_id == p.strip()), None)
            if pc: c.addPrerequisite(pc)
    admin_service.create_course(c)
    courses_data.append(c)
    offerings[c.course_id] = CourseOffering(c.course_id, c.capacity)
    facades[c.course_id] = EnrollmentFacade(event_publisher, offerings[c.course_id], repository, schedule, course_repo, user_repo, offerings)
    return jsonify({"status": "success", "message": "Course created successfully."})

@app.route('/api/admin/users/deactivate', methods=['POST'])
def deactivate_user_api():
    uid = request.json['id']
    admin_service.deactivate_user(str(uid))
    return jsonify({"status": "success"})

@app.route('/api/admin/programs', methods=['POST'])
def add_program():
    data = request.json
    from models.course import DegreeProgram
    req_courses = [c.strip() for c in data.get('required_courses', '').split(',')] if data.get('required_courses') else []
    admin_service.define_program(DegreeProgram(data['id'], data['name'], int(data['credits']), req_courses))
    return jsonify({"status": "success"})

@app.route('/api/instructure/change-desc', methods=['POST'])
def change_desc():
    data = request.json
    from patterns.command import UpdateDescriptionCommand, CourseChangeRequest
    import uuid
    course = next((c for c in courses_data if c.course_id == str(data['course_id'])), None)
    req_id = str(uuid.uuid4())[:8]
    req = CourseChangeRequest(req_id, course.course_id, data['instructure_id'], UpdateDescriptionCommand(course, data['desc']))
    instructure_service.submit_course_change_request(req, admin_service)
    admin_service.approve_course_change_request(req_id)
    return jsonify({"status": "success", "message": "Description update requested and auto-approved."})

@app.route('/api/instructure/change-prereq', methods=['POST'])
def change_prereq():
    data = request.json
    from patterns.command import AddPrerequisiteCommand, CourseChangeRequest
    import uuid
    course = next((c for c in courses_data if c.course_id == str(data['course_id'])), None)
    prereq_course = next((c for c in courses_data if c.course_id == str(data['prereq_id'])), None)
    if prereq_course:
        req_id = str(uuid.uuid4())[:8]
        req = CourseChangeRequest(req_id, course.course_id, data['instructure_id'], AddPrerequisiteCommand(course, prereq_course))
        instructure_service.submit_course_change_request(req, admin_service)
        admin_service.approve_course_change_request(req_id)
    return jsonify({"status": "success", "message": "Prerequisite change requested and auto-approved."})

@app.route('/api/instructure/change-schedule', methods=['POST'])
def change_schedule():
    data = request.json
    from patterns.command import ChangeScheduleCommand, CourseChangeRequest
    import uuid
    course = next((c for c in courses_data if c.course_id == str(data['course_id'])), None)
    if course:
        req_id = str(uuid.uuid4())[:8]
        req = CourseChangeRequest(req_id, course.course_id, data['instructure_id'], ChangeScheduleCommand(course, data['schedule']))
        instructure_service.submit_course_change_request(req, admin_service)
        admin_service.approve_course_change_request(req_id)
    return jsonify({"status": "success", "message": "Schedule change requested and auto-approved."})

@app.route('/api/admin/users/add', methods=['POST'])
def add_user_api():
    data = request.json
    role = data['role']
    email = data['email']
    if role == 'student':
        u = student_creator.registerUser(UserDetails(data['id'], data['name'], email))
    else:
        u = instructure_creator.registerUser(UserDetails(data['id'], data['name'], email))
    u.role = role
    admin_service.add_user(u)
    return jsonify({"status": "success"})

@app.route('/api/admin/users/edit', methods=['POST'])
def edit_user_api():
    data = request.json
    uid = data['id']
    for u in admin_service.users:
        if u.id == uid:
            if 'name' in data: u._name = data['name']
            if 'email' in data: u._email = data['email']
            if 'role' in data: u.role = data['role']
            break
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

@app.route('/api/admin/force_add', methods=['POST'])
def force_add_api():
    data = request.json
    facade = facades.get(data['course_id'])
    if facade:
        res = facade.force_enroll(data['student_id'], data['course_id'])
        if res.name == 'SUCCESS':
            student = next((s for s in admin_service.users if s.id == data['student_id']), None)
            if student and data['course_id'] not in student.enrolled_courses:
                student.enrolled_courses.append(data['course_id'])
            return jsonify({"status": "success"})
    return jsonify({"status": "failed"}), 400

@app.route('/api/admin/assign_course', methods=['POST'])
def assign_course_api():
    data = request.json
    c = next((cx for cx in courses_data if cx.course_id == data['course_id']), None)
    if c:
        c.instructor_id = data['instructure_id']
        return jsonify({"status": "success"})
    return jsonify({"status": "failed"}), 404

@app.route('/api/admin/reports/high_capacity', methods=['POST'])
def high_capacity_report():
    data = request.json
    from patterns.template_method import HighCapacityReport
    report_gen = HighCapacityReport(data['department'], int(data['threshold']), courses_data, offerings)
    report = report_gen.generateReport()
    return jsonify({"status": "success", "content": report.content})

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)

@app.route('/api/programs', methods=['GET'])
def get_programs():
    return jsonify(programs_data)

@app.route('/api/programs', methods=['POST'])
def update_programs():
    data = request.json
    global programs_data
    programs_data = data
    return jsonify({"status": "success", "message": "Programs updated successfully."})
