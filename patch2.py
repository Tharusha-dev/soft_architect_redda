import re

with open("frontend/app.js", "r") as f:
    js = f.read()

# 1. Fix Student Progress (Waitlist & Past Semesters)
student_old = """        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fa-solid fa-graduation-cap"></i></div>
                <div class="stat-info">
                    <h3>Credits Earned</h3>
                    <div class="stat-value">${db.student.completedCourses.length * 3} / 120</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fa-solid fa-star"></i></div>
                <div class="stat-info">
                    <h3>Current GPA</h3>
                    <div class="stat-value">${gpa}</div>
                </div>
            </div>
        </div>

        <div class="mb-6">
            <h3 class="section-title">Completed Courses</h3>
        </div>"""

student_new = """        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fa-solid fa-graduation-cap"></i></div>
                <div class="stat-info">
                    <h3>Credits Earned</h3>
                    <div class="stat-value">${db.student.completedCourses.length * 3} / 120</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fa-solid fa-star"></i></div>
                <div class="stat-info">
                    <h3>Current GPA</h3>
                    <div class="stat-value">${gpa}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #FEF3C7; color: #D97706;"><i class="fa-solid fa-clock"></i></div>
                <div class="stat-info">
                    <h3>Waitlisted</h3>
                    <div class="stat-value">${db.student.waitlistedCourses ? db.student.waitlistedCourses.length : 0}</div>
                </div>
            </div>
        </div>

        <div class="mb-6 mt-6">
            <h3 class="section-title">Past Semester Schedules</h3>
            <p style="color: var(--text-muted); font-size: 0.875rem;">No past semesters found in DB.</p>
            <p style="color: var(--text-muted); font-size: 0.875rem;"><i>Note: The backend maintains completed courses, but lacks full historical semester block storage.</i></p>
        </div>

        <div class="mb-6 mt-6">
            <h3 class="section-title">Completed Courses</h3>
        </div>"""

js = js.replace(student_old, student_new)

# 2. Fix Instructor (Desc & Prereq buttons)
inst_old = """                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-primary" style="flex:1;" onclick="currentView='roster'; renderNav(); renderView();">View Roster</button>
                    <button class="btn btn-outline" style="flex:1;" onclick="requestCapacityChange('${course.id}')">Request Capacity Change</button>
                </div>"""

inst_new = """                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button class="btn btn-primary" style="flex:1; min-width: 120px;" onclick="currentView='roster'; renderNav(); renderView();">View Roster</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestCapacityChange('${course.id}')">Req Capacity</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestDescChange('${course.id}')">Req Desc Change</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestPrereqChange('${course.id}')">Add Prerequisite</button>
                </div>"""

js = js.replace(inst_old, inst_new)

# 3. Fix Admin (Dashboards)
admin_old = """        <div class="grid-cards" style="grid-template-columns: 2fr 1fr;">
            <div class="glass-card">
                <h3 class="section-title">Pending Administrator Approvals</h3>"""

admin_new = """        <div class="grid-cards" style="grid-template-columns: 1fr; margin-bottom: 2rem;">
            <div class="glass-card">
                <h3 class="section-title">Admin CRUD Dashboards</h3>
                <div style="display: flex; gap: 1rem;">
                    <button class="btn btn-secondary" onclick="alert('Degree Programs CRUD UI Placeholder')">Degree Programs (${db.admin.programs ? db.admin.programs.length : 0})</button>
                    <button class="btn btn-secondary" onclick="alert('User Management CRUD UI Placeholder')">Manage Users (${db.admin.users ? db.admin.users.length : 0})</button>
                    <button class="btn btn-secondary" onclick="alert('Course Management CRUD UI Placeholder')">Manage Courses (${db.admin.courses ? db.admin.courses.length : 0})</button>
                </div>
            </div>
        </div>

        <div class="grid-cards" style="grid-template-columns: 2fr 1fr;">
            <div class="glass-card">
                <h3 class="section-title">Pending Administrator Approvals</h3>"""

js = js.replace(admin_old, admin_new)

# Add prompt functions for new instructure commands
js += """
async function requestDescChange(courseId) {
    const desc = prompt("Enter new description:");
    if(!desc) return;
    await fetch(`${API_URL}/instructure/change-desc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: db.instructure.id, course_id: courseId, desc: desc })
    });
    alert("Description Update Request Sent!");
    fetchState();
}

async function requestPrereqChange(courseId) {
    const prereq = prompt("Enter prerequisite course ID:");
    if(!prereq) return;
    await fetch(`${API_URL}/instructure/change-prereq`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: db.instructure.id, course_id: courseId, prereq_id: prereq })
    });
    alert("Prerequisite Update Request Sent!");
    fetchState();
}
"""

with open("frontend/app.js", "w") as f:
    f.write(js)
print("Second patch applied.")
