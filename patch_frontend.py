import re

# 1. Update api.py
with open("api.py", "r") as f:
    api_content = f.read()

# Add Notifications
notification_code = """
notifications_db = []
class APINotificationObserver:
    def update(self, event):
        notifications_db.insert(0, {"type": event.type, "payload": event.payload, "timestamp": "Just now"})

event_publisher.subscribe("WAITLIST_JOINED", APINotificationObserver())
event_publisher.subscribe("WAITLIST_PROMOTED", APINotificationObserver())
event_publisher.subscribe("ENROLLMENT_SUCCESS", APINotificationObserver())
event_publisher.subscribe("COURSE_DROPPED", APINotificationObserver())

@app.route('/api/notifications/<user_id>', methods=['GET'])
def get_notifications(user_id):
    user_notifs = [n for n in notifications_db if str(n['payload'].get('student_id')) == str(user_id) or str(n['payload'].get('instructure_id')) == str(user_id)]
    return jsonify(user_notifs)
"""
api_content = api_content.replace(
    "notification_service = NotificationService()\nevent_publisher = notification_service.get_publisher()",
    "notification_service = NotificationService()\nevent_publisher = notification_service.get_publisher()\n" + notification_code
)

# Update get_state
api_content = api_content.replace(
"""        "student": {
            "id": s1.id,
            "name": s1.name,
            "completedCourses": [{"id": get_course_code(k), "grade": v} for k, v in s1.completed_courses.items()],
            "enrolledCourses": [int(c) for c in s1.enrolled_courses]
        },""",
"""        "student": {
            "id": s1.id,
            "name": s1.name,
            "completedCourses": [{"id": get_course_code(k), "grade": v} for k, v in s1.completed_courses.items()],
            "enrolledCourses": [int(c) for c in s1.enrolled_courses],
            "waitlistedCourses": [int(c.course_id) for c in courses_data if s1.id in offerings[c.course_id].waitlist]
        },"""
)

api_content = api_content.replace(
"""        "admin": {
            "pending_requests": [
                {"id": req.request_id, "course_id": req.course_id} 
                for req in admin_service.pending_course_requests
            ],""",
"""        "admin": {
            "courses": [{"id": c.course_id, "name": c.name} for c in admin_service.courses],
            "users": [{"id": u.id, "name": u._name, "active": u.is_active} for u in admin_service.users],
            "programs": [{"id": p.id, "name": p.name} for p in admin_service.programs],
            "pending_requests": [
                {"id": req.request_id, "course_id": req.course_id} 
                for req in admin_service.pending_course_requests
            ],"""
)

# Admin Endpoints
admin_endpoints = """
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
"""
api_content += admin_endpoints

# Instructure Endpoints
instructure_endpoints = """
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
"""
api_content += instructure_endpoints

with open("api.py", "w") as f:
    f.write(api_content)


# 2. Update frontend/index.html
with open("frontend/index.html", "r") as f:
    html = f.read()

html = html.replace(
"""                <div class="header-actions">
                </div>""",
"""                <div class="header-actions">
                    <button class="btn btn-secondary" onclick="showNotifications()">🔔 Notifications</button>
                </div>"""
)
with open("frontend/index.html", "w") as f:
    f.write(html)


# 3. Update frontend/app.js
with open("frontend/app.js", "r") as f:
    js = f.read()

js += """
async function showNotifications() {
    let uid = state.role === 'student' ? state.student.id : (state.role === 'instructure' ? state.instructure.id : 'admin');
    const res = await fetch(`${API_URL}/notifications/${uid}`);
    const notifs = await res.json();
    let msg = notifs.length ? notifs.map(n => `[${n.type}] ${JSON.stringify(n.payload)}`).join('\\n') : "No notifications.";
    alert(msg);
}
"""

js = js.replace(
"""        <div class="stat-card">
            <h3>Completed Courses</h3>
            <div class="stat-value">${Object.keys(state.student.completedCourses).length}</div>
        </div>
    </div>""",
"""        <div class="stat-card">
            <h3>Completed Courses</h3>
            <div class="stat-value">${Object.keys(state.student.completedCourses).length}</div>
        </div>
        <div class="stat-card">
            <h3>Waitlisted Courses</h3>
            <div class="stat-value">${state.student.waitlistedCourses.length}</div>
        </div>
    </div>
    
    <div class="card mt-2">
        <h3>Past Semester Schedules</h3>
        <p>No past semesters found in DB.</p>
        <p><i>Note: The backend maintains completed courses, but lacks full historical semester block storage.</i></p>
    </div>
"""
)

js = js.replace(
"""            <h3>Request Course Change</h3>
            <div class="form-group">
                <label>Course ID</label>
                <input type="text" id="change-course-id" class="search-input">
            </div>
            <div class="form-group">
                <label>New Capacity</label>
                <input type="number" id="change-capacity" class="search-input">
            </div>
            <button class="btn btn-primary" onclick="submitChangeRequest()">Submit Request (Command Pattern)</button>""",
"""            <h3>Request Course Change</h3>
            <div class="form-group">
                <label>Course ID</label>
                <input type="text" id="change-course-id" class="search-input">
            </div>
            <div class="form-group">
                <label>New Capacity</label>
                <input type="number" id="change-capacity" class="search-input">
                <button class="btn btn-primary" onclick="submitChangeRequest()">Update Capacity</button>
            </div>
            <div class="form-group">
                <label>New Description</label>
                <input type="text" id="change-desc" class="search-input">
                <button class="btn btn-primary" onclick="submitDescRequest()">Update Description</button>
            </div>
            <div class="form-group">
                <label>Add Prerequisite ID</label>
                <input type="text" id="change-prereq" class="search-input">
                <button class="btn btn-primary" onclick="submitPrereqRequest()">Add Prereq</button>
            </div>"""
)

js += """
async function submitDescRequest() {
    const courseId = document.getElementById('change-course-id').value;
    const desc = document.getElementById('change-desc').value;
    await fetch(`${API_URL}/instructure/change-desc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: state.instructure.id, course_id: courseId, desc: desc })
    });
    alert("Description Update Request Sent!");
    fetchState();
}
async function submitPrereqRequest() {
    const courseId = document.getElementById('change-course-id').value;
    const prereq = document.getElementById('change-prereq').value;
    await fetch(`${API_URL}/instructure/change-prereq`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: state.instructure.id, course_id: courseId, prereq_id: prereq })
    });
    alert("Prerequisite Update Request Sent!");
    fetchState();
}
"""

js = js.replace(
"""    container.innerHTML = `
        <div class="grid" style="grid-template-columns: 1fr; margin-bottom: 2rem;">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3>Pending Administrative Approvals</h3>""",
"""    container.innerHTML = `
        <div class="grid" style="grid-template-columns: 1fr; margin-bottom: 2rem;">
            <div class="card">
                <h3>Admin CRUD Dashboards</h3>
                <button class="btn btn-secondary" onclick="alert('Degree Programs CRUD UI Placeholder')">Degree Programs (${state.admin.programs.length})</button>
                <button class="btn btn-secondary" onclick="alert('User Management CRUD UI Placeholder')">Manage Users (${state.admin.users.length})</button>
                <button class="btn btn-secondary" onclick="alert('Course Management CRUD UI Placeholder')">Manage Courses (${state.admin.courses.length})</button>
            </div>
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <h3>Pending Administrative Approvals</h3>"""
)

with open("frontend/app.js", "w") as f:
    f.write(js)

print("UI Patch Applied!")
