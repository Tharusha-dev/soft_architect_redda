import re

# --- API.PY PATCH ---
with open("api.py", "r") as f:
    api_content = f.read()

# Add mock data to admin_service
api_content = api_content.replace(
"""admin_service = AdminService()
instructure_service = InstructureService()""",
"""admin_service = AdminService()
instructure_service = InstructureService()

# Populate Admin Service Memory
for u in [s1, s2, s3, s4, f1]:
    admin_service.add_user(u)
for c in courses_data:
    admin_service.create_course(c)
from models.course import DegreeProgram
admin_service.define_program(DegreeProgram("CS-BS", "BSc Computer Science", 120, []))
"""
)

# Add edit/add endpoints
admin_endpoints = """
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
"""

if "/api/admin/users/add" not in api_content:
    api_content += admin_endpoints

with open("api.py", "w") as f:
    f.write(api_content)

# --- APP.JS PATCH ---
with open("frontend/app.js", "r") as f:
    js = f.read()

# Route views in renderView
js = js.replace(
"""        case 'reports':
            renderAdminReports();
            break;""",
"""        case 'reports':
            renderAdminReports();
            break;
        case 'admin_users':
            renderAdminUsers();
            break;
        case 'admin_courses':
            renderAdminCoursesCRUD();
            break;
        case 'admin_programs':
            renderAdminPrograms();
            break;"""
)

# Update Admin Dashboard buttons
js = js.replace(
"""                    <button class="btn btn-secondary" onclick="managePrograms()">Degree Programs (${db.admin.programs ? db.admin.programs.length : 0})</button>
                    <button class="btn btn-secondary" onclick="manageUsers()">Manage Users (${db.admin.users ? db.admin.users.length : 0})</button>
                    <button class="btn btn-secondary" onclick="manageCourses()">Manage Courses (${db.admin.courses ? db.admin.courses.length : 0})</button>""",
"""                    <button class="btn btn-secondary" onclick="currentView='admin_programs'; renderNav(); renderView();">Degree Programs (${db.admin.programs ? db.admin.programs.length : 0})</button>
                    <button class="btn btn-secondary" onclick="currentView='admin_users'; renderNav(); renderView();">Manage Users (${db.admin.users ? db.admin.users.length : 0})</button>
                    <button class="btn btn-secondary" onclick="currentView='admin_courses'; renderNav(); renderView();">Manage Courses (${db.admin.courses ? db.admin.courses.length : 0})</button>"""
)

# Add Render functions for the proper UI
new_ui_functions = """
function renderAdminUsers() {
    let rows = db.admin.users.map(u => `
        <tr>
            <td>${u.id}</td>
            <td>${u.name}</td>
            <td><span class="status-badge ${u.active ? 'status-success' : 'status-danger'}">${u.active ? 'Active' : 'Deactivated'}</span></td>
            <td>
                <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="editUserUI('${u.id}', '${u.name}')">Edit</button>
                ${u.active ? `<button class="btn btn-primary" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="deactivateUserUI('${u.id}')">Deactivate</button>` : ''}
            </td>
        </tr>
    `).join('');

    viewContainer.innerHTML = `
        <div class="mb-6" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="section-title">Manage Users</h3>
            <button class="btn btn-secondary" onclick="currentView='dashboard'; renderNav(); renderView();">Back to Dashboard</button>
        </div>
        
        <div class="glass-card mb-6">
            <h3>Add New User</h3>
            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <input type="text" id="add-uid" class="search-input" placeholder="User ID">
                <input type="text" id="add-uname" class="search-input" placeholder="Full Name">
                <select id="add-urole" class="search-input"><option value="student">Student</option><option value="instructure">Instructure</option></select>
                <button class="btn btn-primary" onclick="addUserUI()">Create User</button>
            </div>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <thead><tr><th>ID</th><th>Name</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}

async function addUserUI() {
    const id = document.getElementById('add-uid').value;
    const name = document.getElementById('add-uname').value;
    const role = document.getElementById('add-urole').value;
    if(!id || !name) return alert("Fill fields");
    await fetch(`${API_URL}/admin/users/add`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name, role}) });
    await fetchState(); renderView();
}
async function editUserUI(id, oldName) {
    const name = prompt("Enter new name for " + id + ":", oldName);
    if(!name) return;
    await fetch(`${API_URL}/admin/users/edit`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name}) });
    await fetchState(); renderView();
}
async function deactivateUserUI(id) {
    if(!confirm("Deactivate " + id + "?")) return;
    await fetch(`${API_URL}/admin/users/deactivate`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id}) });
    await fetchState(); renderView();
}

function renderAdminCoursesCRUD() {
    let rows = db.admin.courses.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>
                <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="editCourseUI('${c.id}', '${c.name}')">Edit</button>
            </td>
        </tr>
    `).join('');

    viewContainer.innerHTML = `
        <div class="mb-6" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="section-title">Manage Courses</h3>
            <button class="btn btn-secondary" onclick="currentView='dashboard'; renderNav(); renderView();">Back to Dashboard</button>
        </div>
        
        <div class="glass-card mb-6">
            <h3>Add New Course</h3>
            <div style="display: flex; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
                <input type="text" id="add-cid" class="search-input" placeholder="Course ID (e.g. 6)">
                <input type="text" id="add-cname" class="search-input" placeholder="Course Name">
                <input type="number" id="add-ccap" class="search-input" placeholder="Capacity">
                <button class="btn btn-primary" onclick="addCourseUI()">Create Course</button>
            </div>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <thead><tr><th>ID</th><th>Name</th><th>Actions</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}

async function addCourseUI() {
    const id = document.getElementById('add-cid').value;
    const name = document.getElementById('add-cname').value;
    const cap = document.getElementById('add-ccap').value;
    if(!id || !name || !cap) return alert("Fill fields");
    await fetch(`${API_URL}/admin/courses`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name, desc: name, instructor: 'Staff', capacity: parseInt(cap), schedule: 'TBD'}) });
    await fetchState(); renderView();
}
async function editCourseUI(id, oldName) {
    const name = prompt("Enter new name for " + id + ":", oldName);
    const cap = prompt("Enter new capacity:");
    if(!name || !cap) return;
    await fetch(`${API_URL}/admin/courses/edit`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name, capacity: cap}) });
    await fetchState(); renderView();
}

function renderAdminPrograms() {
    let rows = db.admin.programs.map(p => `
        <tr><td>${p.id}</td><td>${p.name}</td></tr>
    `).join('');
    viewContainer.innerHTML = `
        <div class="mb-6" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="section-title">Degree Programs</h3>
            <button class="btn btn-secondary" onclick="currentView='dashboard'; renderNav(); renderView();">Back to Dashboard</button>
        </div>
        
        <div class="glass-card mb-6">
            <h3>Add New Program</h3>
            <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                <input type="text" id="add-pid" class="search-input" placeholder="Program ID">
                <input type="text" id="add-pname" class="search-input" placeholder="Program Name">
                <button class="btn btn-primary" onclick="addProgramUI()">Create Program</button>
            </div>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <thead><tr><th>ID</th><th>Name</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}
async function addProgramUI() {
    const id = document.getElementById('add-pid').value;
    const name = document.getElementById('add-pname').value;
    if(!id || !name) return alert("Fill fields");
    await fetch(`${API_URL}/admin/programs`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name}) });
    await fetchState(); renderView();
}
"""

if "function renderAdminUsers" not in js:
    js += new_ui_functions

with open("frontend/app.js", "w") as f:
    f.write(js)

print("Fourth patch applied: Built full UI components for Admin CRUD.")
