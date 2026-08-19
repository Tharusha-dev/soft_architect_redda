
// --- CUSTOM UI MODALS ---
function uiAlert(msg) {
    return new Promise(resolve => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;backdrop-filter:blur(4px);';
        const box = document.createElement('div');
        box.className = 'glass-card';
        box.style.cssText = 'background:var(--card-bg);padding:2rem;border-radius:1rem;min-width:300px;text-align:center;box-shadow:0 10px 25px rgba(0,0,0,0.2);max-width:80%;max-height:80%;overflow-y:auto;';
        
        const text = document.createElement('div');
        text.style.whiteSpace = 'pre-wrap';
        text.textContent = msg;
        text.style.marginBottom = '1.5rem';
        
        const btn = document.createElement('button');
        btn.className = 'btn btn-primary';
        btn.textContent = 'OK';
        btn.onclick = () => { overlay.remove(); resolve(); };
        
        box.appendChild(text);
        box.appendChild(btn);
        overlay.appendChild(box);
        document.body.appendChild(overlay);
        btn.focus();
    });
}

function uiConfirm(msg) {
    return new Promise(resolve => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;backdrop-filter:blur(4px);';
        const box = document.createElement('div');
        box.className = 'glass-card';
        box.style.cssText = 'background:var(--card-bg);padding:2rem;border-radius:1rem;min-width:300px;text-align:center;box-shadow:0 10px 25px rgba(0,0,0,0.2);';
        
        const text = document.createElement('div');
        text.style.marginBottom = '1.5rem';
        text.textContent = msg;
        
        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'display:flex;gap:1rem;justify-content:center;';
        
        const yesBtn = document.createElement('button');
        yesBtn.className = 'btn btn-danger';
        yesBtn.textContent = 'Confirm';
        yesBtn.onclick = () => { overlay.remove(); resolve(true); };
        
        const noBtn = document.createElement('button');
        noBtn.className = 'btn btn-secondary';
        noBtn.textContent = 'Cancel';
        noBtn.onclick = () => { overlay.remove(); resolve(false); };
        
        btnContainer.appendChild(yesBtn);
        btnContainer.appendChild(noBtn);
        box.appendChild(text);
        box.appendChild(btnContainer);
        overlay.appendChild(box);
        document.body.appendChild(overlay);
    });
}

function uiPrompt(msg, defaultVal='') {
    return new Promise(resolve => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;backdrop-filter:blur(4px);';
        const box = document.createElement('div');
        box.className = 'glass-card';
        box.style.cssText = 'background:var(--card-bg);padding:2rem;border-radius:1rem;min-width:300px;text-align:center;box-shadow:0 10px 25px rgba(0,0,0,0.2);';
        
        const text = document.createElement('div');
        text.style.marginBottom = '1rem';
        text.textContent = msg;
        
        const input = document.createElement('input');
        input.type = 'text';
        input.className = 'search-input';
        input.value = defaultVal || '';
        input.style.marginBottom = '1.5rem';
        input.style.width = '100%';
        
        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'display:flex;gap:1rem;justify-content:center;';
        
        const yesBtn = document.createElement('button');
        yesBtn.className = 'btn btn-primary';
        yesBtn.textContent = 'Submit';
        yesBtn.onclick = () => { overlay.remove(); resolve(input.value); };
        
        const noBtn = document.createElement('button');
        noBtn.className = 'btn btn-secondary';
        noBtn.textContent = 'Cancel';
        noBtn.onclick = () => { overlay.remove(); resolve(null); };
        
        btnContainer.appendChild(yesBtn);
        btnContainer.appendChild(noBtn);
        box.appendChild(text);
        box.appendChild(input);
        box.appendChild(btnContainer);
        overlay.appendChild(box);
        document.body.appendChild(overlay);
        input.focus();
    });
}

// Data will be fetched from API
let db = {};

async function fetchState() {
    try {
        const res = await fetch('http://localhost:5000/api/state');
        db = await res.json();
    } catch (e) {
        console.error("Failed to fetch state from API. Ensure python3 api.py is running.", e);
        showToast('Failed to connect to API backend.', 'error');
    }
}

// UI Elements
const roleSelect = document.getElementById('role-select');
const sidebarNav = document.getElementById('sidebar-nav');
const viewContainer = document.getElementById('view-container');
const pageTitle = document.getElementById('page-title');
const userName = document.getElementById('user-name');
const userId = document.getElementById('user-id');
const userAvatar = document.getElementById('user-avatar');
const toastContainer = document.getElementById('toast-container');

// Navigation Config
const navConfig = {
    student: [
        { id: 'browse', icon: 'fa-book-open', label: 'Course Catalogue' },
        { id: 'schedule', icon: 'fa-calendar-days', label: 'My Schedule' },
        { id: 'progress', icon: 'fa-chart-line', label: 'Academic Progress' }
    ],
    instructure: [
        { id: 'my-classes', icon: 'fa-chalkboard-user', label: 'My Classes' },
        { id: 'roster', icon: 'fa-users', label: 'Class Roster' },
        { id: 'grading', icon: 'fa-pen-to-square', label: 'Grade Submission' }
    ],
    admin: [
        { id: 'dashboard', icon: 'fa-chart-pie', label: 'Dashboard' },
        { id: 'courses', icon: 'fa-layer-group', label: 'Course Management' },
        { id: 'reports', icon: 'fa-file-invoice', label: 'Reports & Analytics' }
    ]
};

// State
let currentRole = 'student';
let currentView = 'browse';

// Initialization
async function init() {
    await fetchState();
    
    roleSelect.addEventListener('change', async (e) => {
        currentRole = e.target.value;
        updateUserIdentity();
        renderNav();
        // Load default view for role
        currentView = navConfig[currentRole][0].id;
        await fetchState();
        renderView();
        showToast(`Switched to ${currentRole.charAt(0).toUpperCase() + currentRole.slice(1)} view`, 'success');
    });

    updateUserIdentity();
    renderNav();
    renderView();
}

// User Identity
function updateUserIdentity() {
    if (currentRole === 'student') {
        userName.textContent = db.student.name;
        userId.textContent = `ID: ${db.student.id}`;
        userAvatar.textContent = db.student.name.charAt(0);
    } else if (currentRole === 'instructure') {
        userName.textContent = db.instructure.name;
        userId.textContent = `ID: ${db.instructure.id}`;
        userAvatar.textContent = db.instructure.name.charAt(0);
    } else {
        userName.textContent = 'System Admin';
        userId.textContent = 'ID: ADMIN-01';
        userAvatar.textContent = 'A';
    }
}

// Render Sidebar Navigation
function renderNav() {
    sidebarNav.innerHTML = '';
    const items = navConfig[currentRole];
    
    items.forEach(item => {
        const a = document.createElement('a');
        a.className = `nav-item ${item.id === currentView ? 'active' : ''}`;
        a.innerHTML = `<i class="fa-solid ${item.icon}"></i> ${item.label}`;
        a.addEventListener('click', (e) => {
            e.preventDefault();
            currentView = item.id;
            // Update active class
            document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
            a.classList.add('active');
            renderView();
        });
        sidebarNav.appendChild(a);
    });
}

// Main Router / Renderer
function renderView() {
    const activeNavItem = navConfig[currentRole].find(n => n.id === currentView);
    pageTitle.textContent = activeNavItem ? activeNavItem.label : 'Dashboard';
    
    viewContainer.innerHTML = ''; // Clear current view
    
    // Router logic
    if (currentRole === 'student') {
        if (currentView === 'browse') renderStudentBrowse();
        else if (currentView === 'schedule') renderStudentSchedule();
        else if (currentView === 'progress') renderStudentProgress();
    } else if (currentRole === 'instructure') {
        if (currentView === 'my-classes') renderInstructureClasses();
        else if (currentView === 'roster') renderInstructureRoster();
        else if (currentView === 'grading') renderInstructureGrading();
    } else if (currentRole === 'admin') {
        if (currentView === 'dashboard') renderAdminDashboard();
        else if (currentView === 'courses') renderAdminCoursesCRUD();
        else if (currentView === 'reports') renderAdminReports();
        else if (currentView === 'admin_users') renderAdminUsers();
        else if (currentView === 'admin_courses') renderAdminCoursesCRUD();
        else if (currentView === 'admin_programs') renderAdminPrograms();
    }
}

// --- STUDENT VIEWS ---

function renderStudentBrowse() {
    const html = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Available Courses</h3>
        </div>
        <div class="grid-cards" id="course-grid"></div>
    `;
    viewContainer.innerHTML = html;
    
    const grid = document.getElementById('course-grid');
    
    db.courses.forEach(course => {
        const isEnrolled = db.student.enrolledCourses.includes(course.id);
        const isFull = course.enrolled >= course.capacity;
        
        let actionBtn = `<button class="btn btn-primary" onclick="enrolCourse(${course.id})">Enrol Now</button>`;
        if (isEnrolled) {
            actionBtn = `<button class="btn btn-danger" onclick="dropCourse(${course.id})">Drop Course</button>`;
        } else if (isFull) {
            actionBtn = `<button class="btn btn-disabled" disabled>Waitlist</button>`;
        }

        const capacityPercentage = (course.enrolled / course.capacity) * 100;
        
        grid.innerHTML += `
            <div class="glass-card course-card">
                <div class="course-header">
                    <span class="course-code">${course.code}</span>
                    ${isEnrolled ? '<span class="status-badge status-success">Enrolled</span>' : ''}
                    ${!isEnrolled && isFull ? '<span class="status-badge status-warning">Full</span>' : ''}
                </div>
                <h3 class="course-title">${course.title}</h3>
                <div class="course-meta">
                    <div class="meta-item"><i class="fa-solid fa-user-tie"></i> ${course.instructor}</div>
                    <div class="meta-item"><i class="fa-solid fa-clock"></i> ${course.schedule}</div>
                    <div class="meta-item"><i class="fa-solid fa-award"></i> ${course.credits} Credits</div>
                </div>
                
                <div class="progress-container mb-6">
                    <div class="progress-header">
                        <span>Capacity</span>
                        <span>${course.enrolled} / ${course.capacity} Seats</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill ${isFull ? 'full' : ''}" style="width: ${capacityPercentage}%"></div>
                    </div>
                </div>
                
                ${actionBtn}
            </div>
        `;
    });
}

async function enrolCourse(courseId) {
    showToast('Processing enrolment transaction via Python Core...', 'warning');
    
    try {
        const res = await fetch('http://localhost:5000/api/enroll', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ student_id: db.student.id, course_id: courseId })
        });
        const data = await res.json();
        
        if (res.ok) {
            showToast(data.message, 'success');
            await fetchState(); // Sync state from python backend
            renderStudentBrowse(); // Re-render
        } else {
            showToast(data.message, 'error');
        }
    } catch (e) {
        showToast('API Connection Error', 'error');
    }
}

async function dropCourse(courseId) {
    showToast('Processing drop request via Python Core...', 'warning');
    
    try {
        const res = await fetch('http://localhost:5000/api/drop', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ student_id: db.student.id, course_id: courseId })
        });
        const data = await res.json();
        
        if (res.ok) {
            showToast(data.message, 'success');
            await fetchState(); // Sync state from python backend
            renderStudentBrowse();
        } else {
            showToast(data.message, 'error');
        }
    } catch (e) {
        showToast('API Connection Error', 'error');
    }
}

function renderStudentSchedule() {
    const enrolledCourses = db.courses.filter(c => db.student.enrolledCourses.includes(c.id));
    
    if (enrolledCourses.length === 0) {
        viewContainer.innerHTML = `
            <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
                <i class="fa-regular fa-calendar-xmark" style="font-size: 4rem; color: var(--text-light); margin-bottom: 1rem;"></i>
                <h3 style="color: var(--text-muted);">No courses scheduled</h3>
                <p style="color: var(--text-light); margin-top: 0.5rem; margin-bottom: 1.5rem;">You haven't enrolled in any courses for this semester.</p>
                <button class="btn btn-primary" onclick="currentView='browse'; renderNav(); renderView();">Browse Courses</button>
            </div>
        `;
        return;
    }

    let rows = enrolledCourses.map(course => `
        <tr>
            <td><strong>${course.code}</strong></td>
            <td>${course.title}</td>
            <td>${course.schedule}</td>
            <td>${course.instructor}</td>
        </tr>
    `).join('');

    viewContainer.innerHTML = `
        <div class="mb-6">
            <h3 class="section-title">This Week's Schedule</h3>
        </div>
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Course Code</th>
                        <th>Course Name</th>
                        <th>Time & Location</th>
                        <th>Instructor</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
    `;
}

function renderStudentProgress() {
    const gradePoints = { 'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0 };
    let totalPoints = 0;
    
    let completedRows = db.student.completedCourses.map(c => {
        totalPoints += gradePoints[c.grade] || 4.0;
        return `
        <tr>
            <td><strong>${c.id}</strong></td>
            <td>Spring 2026</td>
            <td><span class="status-badge status-success">${c.grade}</span></td>
            <td>3</td>
        </tr>
    `}).join('');

    const gpa = db.student.completedCourses.length ? (totalPoints / db.student.completedCourses.length).toFixed(1) : '0.0';

    viewContainer.innerHTML = `
        <div class="stats-grid">
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
        </div>
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Course Code</th>
                        <th>Term</th>
                        <th>Grade</th>
                        <th>Credits</th>
                    </tr>
                </thead>
                <tbody>
                    ${completedRows}
                </tbody>
            </table>
        </div>
    `;
}

// --- INSTRUCTURE VIEWS ---

function renderInstructureClasses() {
    const taughtCourses = db.courses.filter(c => db.instructure.taughtCourses.includes(c.id));
    
    let html = `<div class="grid-cards">`;
    taughtCourses.forEach(course => {
        html += `
            <div class="glass-card course-card">
                <div class="course-header">
                    <span class="course-code">${course.code}</span>
                    <span class="status-badge status-success">Active</span>
                </div>
                <h3 class="course-title">${course.title}</h3>
                <div class="course-meta">
                    <div class="meta-item"><i class="fa-solid fa-clock"></i> ${course.schedule}</div>
                    <div class="meta-item"><i class="fa-solid fa-users"></i> ${course.enrolled} Students Enrolled</div>
                </div>
                
                <div class="progress-container mb-6">
                    <div class="progress-header">
                        <span>Capacity Filled</span>
                        <span>${Math.round((course.enrolled/course.capacity)*100)}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${(course.enrolled/course.capacity)*100}%"></div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button class="btn btn-primary" style="flex:1; min-width: 120px;" onclick="currentView='roster'; renderNav(); renderView();">View Roster</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestCapacityChange('${course.id}')">Req Capacity</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestDescChange('${course.id}')">Req Desc Change</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestPrereqChange('${course.id}')">Add Prerequisite</button>
                </div>
            </div>
        `;
    });
    html += `</div>`;
    viewContainer.innerHTML = html;
}

function renderInstructureRoster() {
    const instructureCourseId = db.instructure.taughtCourses[0] || 2;
    const courseObj = db.courses.find(c => c.id == instructureCourseId);
    const courseTitle = courseObj ? courseObj.code : 'SCS2303';

    let rows = db.students.map(s => `
        <tr>
            <td><strong>${s.id}</strong></td>
            <td>${s.name}</td>
            <td>${s.name.toLowerCase().replace(' ', '.')}@nexus.edu</td>
            <td><span class="status-badge status-success">Enrolled</span></td>
        </tr>
    `).join('');

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">${courseTitle} - Class Roster</h3>
        </div>
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
    `;
}

function renderInstructureGrading() {
    const instructureCourseId = db.instructure.taughtCourses[0] || 2;
    const courseObj = db.courses.find(c => c.id == instructureCourseId);
    const courseTitle = courseObj ? courseObj.code : 'SCS2303';

    const pendingStudentIds = (db.admin && db.admin.pending_grades) 
        ? db.admin.pending_grades.filter(g => String(g.course_id) == String(instructureCourseId)).map(g => String(g.student_id)) 
        : [];

    let rows = db.students.map(s => {
        const sGrade = s.completedCourses ? s.completedCourses[courseTitle] : '';
        return `
        <tr>
            <td><strong>${s.id}</strong></td>
            <td>${s.name}</td>
            <td>
                <select id="grade-sel-${s.id}" class="form-control grade-select" style="width: 100px; padding: 0.5rem;" onchange="document.getElementById('submit-btn-${s.id}').style.display = 'block'">
                    <option value="">-</option>
                    <option value="A" ${sGrade === 'A' ? 'selected' : ''}>A</option>
                    <option value="B" ${sGrade === 'B' ? 'selected' : ''}>B</option>
                    <option value="C" ${sGrade === 'C' ? 'selected' : ''}>C</option>
                    <option value="F" ${sGrade === 'F' ? 'selected' : ''}>F</option>
                </select>
            </td>
            <td id="status-${s.id}">
                ${sGrade ? '<span class="status-badge status-success">Approved</span>' : pendingStudentIds.includes(String(s.id)) ? '<span class="status-badge status-warning">Pending</span>' : 'Not Submitted'}
            </td>
            <td>
                <button id="submit-btn-${s.id}" class="btn btn-primary" style="display: none; padding: 0.25rem 0.5rem;" onclick="submitSingleGrade('${s.id}', '${instructureCourseId}')">Submit</button>
            </td>
        </tr>
    `}).join('');

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Grade Submission - ${courseTitle}</h3>
        </div>
        <div class="glass-card mb-6" style="background-color: var(--primary-light); border: none; padding: 1rem;">
            <p style="color: var(--primary); font-size: 0.875rem;"><i class="fa-solid fa-circle-info"></i> Grades submitted here will be sent to the administration for final approval before being published to student records.</p>
        </div>
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
    `;
}

async function submitSingleGrade(studentId, courseId) {
    showToast('Validating grade via State Pattern...', 'warning');
    
    const gradeSelect = document.getElementById('grade-sel-' + studentId);
    const grade = gradeSelect ? gradeSelect.value : '';
    
    const res = await fetch('http://localhost:5000/api/instructure/grades/submit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ course_id: courseId || 2, instructure_id: db.instructure.id, student_id: studentId, grade: grade })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    
    await fetchState(); // fetch state silently so db is updated, but don't call renderView to avoid wiping form
    
    // update specific row DOM
    const btn = document.getElementById('submit-btn-' + studentId);
    if (btn) btn.style.display = 'none';
    const statusCell = document.getElementById('status-' + studentId);
    if (statusCell) {
        statusCell.innerHTML = '<span class="status-badge status-warning">Pending</span>';
    }
}

async function requestCapacityChange(courseId) {
    const newCap = await uiPrompt("Enter new capacity for this course:");
    if (!newCap || isNaN(newCap)) return;
    
    showToast('Sending Course Change Request Command...', 'warning');
    
    const res = await fetch('http://localhost:5000/api/instructure/change-capacity', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ course_id: courseId, instructure_id: db.instructure.id, capacity: newCap })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

// --- ADMIN VIEWS ---

function renderAdminDashboard() {
    const totalStudents = db.students ? db.students.length : 4;
    const totalCourses = db.courses.length;
    
    // Calculate real total capacity filled vs available
    const totalCapacity = db.courses.reduce((sum, c) => sum + c.capacity, 0);
    const totalEnrolled = db.courses.reduce((sum, c) => sum + c.enrolled, 0);
    const sysLoad = totalCapacity > 0 ? Math.round((totalEnrolled / totalCapacity) * 100) + '%' : '0%';
    
    let alertsHtml = '';
    db.courses.forEach(c => {
        if (c.enrolled >= c.capacity) {
            alertsHtml += `
            <div style="padding: 1rem; border-left: 3px solid var(--warning); background-color: #FEF3C7; border-radius: 0 0.5rem 0.5rem 0; margin-bottom: 0.5rem;">
                <h4 style="color: var(--warning); font-size: 0.875rem; margin-bottom: 0.25rem;">Course Over Capacity</h4>
                <p style="font-size: 0.75rem; color: var(--text-muted);">${c.code} has reached its capacity of ${c.capacity}.</p>
            </div>`;
        }
    });
    if (!alertsHtml) {
        alertsHtml = `
            <div style="padding: 1rem; border-left: 3px solid var(--success); background-color: #D1FAE5; border-radius: 0 0.5rem 0.5rem 0;">
                <h4 style="color: var(--success); font-size: 0.875rem; margin-bottom: 0.25rem;">System Normal</h4>
                <p style="font-size: 0.75rem; color: var(--text-muted);">All courses are within operating capacity bounds.</p>
            </div>
        `;
    }

    let pendingReqs = db.admin.pending_requests.map(req => `
        <tr>
            <td>Request ${req.id}</td>
            <td>Change Capacity for Course ${req.course_id}</td>
            <td><button class="btn btn-primary" style="padding: 0.25rem 0.5rem;" onclick="approveRequest('${req.id}')">Approve</button></td>
        </tr>
    `).join('');
    
    let pendingGrades = (db.admin.pending_grades || []).map(grade => `
        <tr>
            <td>Grade Submission</td>
            <td>Grade for Course ${grade.course_id} (Student: ${grade.student_id})</td>
            <td><button class="btn btn-primary" style="padding: 0.25rem 0.5rem;" onclick="approveGrades('${grade.course_id}', '${grade.student_id}')">Approve</button></td>
        </tr>
    `).join('');

    pendingReqs += pendingGrades;
    
    if (!pendingReqs) {
        pendingReqs = '<tr><td colspan="3" style="text-align:center; color: var(--text-muted);">No pending approvals</td></tr>';
    }

    viewContainer.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #E0E7FF; color: #4F46E5;"><i class="fa-solid fa-users"></i></div>
                <div class="stat-info">
                    <h3>Total Enrolled</h3>
                    <div class="stat-value">${totalStudents}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #D1FAE5; color: #059669;"><i class="fa-solid fa-layer-group"></i></div>
                <div class="stat-info">
                    <h3>Active Courses</h3>
                    <div class="stat-value">${totalCourses}</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #FEF3C7; color: #D97706;"><i class="fa-solid fa-server"></i></div>
                <div class="stat-info">
                    <h3>System Load</h3>
                    <div class="stat-value">${sysLoad}</div>
                </div>
            </div>
        </div>

        <div class="grid-cards" style="grid-template-columns: 1fr; margin-bottom: 2rem;">
            <div class="glass-card">
                <h3 class="section-title">Admin CRUD Dashboards</h3>
                <div style="display: flex; gap: 1rem;">
                    <button class="btn btn-secondary" onclick="currentView='admin_programs'; renderNav(); renderView();">Degree Programs (${db.admin.programs ? db.admin.programs.length : 0})</button>
                    <button class="btn btn-secondary" onclick="currentView='admin_users'; renderNav(); renderView();">Manage Users (${db.admin.users ? db.admin.users.length : 0})</button>
                    <button class="btn btn-secondary" onclick="currentView='admin_courses'; renderNav(); renderView();">Manage Courses (${db.admin.courses ? db.admin.courses.length : 0})</button>
                </div>
            </div>
        </div>

        <div class="grid-cards" style="grid-template-columns: 2fr 1fr;">
            <div class="glass-card">
                <h3 class="section-title">Pending Administrator Approvals</h3>
                <div class="data-table-container" style="box-shadow: none; border: none;">
                    <table class="data-table">
                        <tbody>
                            ${pendingReqs}
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="glass-card">
                <h3 class="section-title">Alerts</h3>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    ${alertsHtml}
                </div>
            </div>
        </div>
    `;
}

async function approveRequest(reqId) {
    showToast('Executing Command Pattern approval...', 'warning');
    const res = await fetch('http://localhost:5000/api/admin/approve-request', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ request_id: reqId })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

async function approveGrades(courseId, studentId) {
    showToast('Executing State Pattern approval...', 'warning');
    const res = await fetch('http://localhost:5000/api/admin/approve-grades', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ course_id: courseId, student_id: studentId })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

function renderAdminCourses() {
    let rows = db.courses.map(c => {
        const capacityPercentage = (c.enrolled / c.capacity) * 100;
        let capBadge = '<span class="status-badge status-success">Normal</span>';
        if (capacityPercentage >= 100) capBadge = '<span class="status-badge" style="background-color: #FEE2E2; color: #B91C1C;">Full</span>';
        else if (capacityPercentage >= 90) capBadge = '<span class="status-badge status-warning">Near Full</span>';

        return `
        <tr>
            <td><strong>${c.code}</strong></td>
            <td>${c.title}</td>
            <td>${c.instructor}</td>
            <td>${c.enrolled}/${c.capacity}</td>
            <td>${capBadge}</td>
            <td>
                <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="editCourse('${c.id}')"><i class="fa-solid fa-pen"></i></button>
            </td>
        </tr>
    `}).join('');

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Course Catalogue Management</h3>
            <button class="btn btn-primary" onclick="createCourse()"><i class="fa-solid fa-plus"></i> Create Course</button>
        </div>
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Title</th>
                        <th>Instructor</th>
                        <th>Enrolment</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
    `;
}

async function createCourse() {
    const code = prompt("Enter course code (e.g. SCS1234):");
    const title = prompt("Enter course title:");
    const instructor = prompt("Enter instructor ID (e.g. F105):");
    const capacity = prompt("Enter capacity:");
    if (!code || !title) return;

    showToast('Creating course...', 'warning');
    const res = await fetch('http://localhost:5000/api/admin/courses', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ code, title, instructor, capacity })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

async function editCourse(courseId) {
    const code = prompt("Enter new course code:");
    const title = prompt("Enter new course title:");
    if (!code || !title) return;

    showToast('Editing course...', 'warning');
    const res = await fetch('http://localhost:5000/api/admin/courses/edit', {
        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id: courseId, code, title })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

function renderAdminReports() {
    viewContainer.innerHTML = `
        <div class="mb-6">
            <h3 class="section-title">Reporting & Analytics</h3>
        </div>
        <div class="grid-cards">
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-chart-line" style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Enrolment Trends</h4>
                <button class="btn btn-primary" onclick="generateReport('stats')">Generate Report</button>
            </div>
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-user-graduate" style="font-size: 3rem; color: var(--accent); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Instructure Workload</h4>
                <button class="btn btn-primary" onclick="generateReport('workload')">Generate Report</button>
            </div>
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-fire" style="font-size: 3rem; color: var(--warning); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Course Popularity</h4>
                <button class="btn btn-primary" onclick="generateReport('popularity')">Generate Report</button>
            </div>
        </div>
        
        <div id="report-output-container" class="glass-card" style="margin-top: 2rem; display: none;">
            <h3 class="section-title" id="report-title">Report Title</h3>
            <pre id="report-content" style="background: var(--bg-color); padding: 1.5rem; border-radius: 0.5rem; white-space: pre-wrap; font-family: monospace; border-left: 4px solid var(--primary);"></pre>
        </div>
    `;
}

async function generateReport(type) {
    showToast('Generating report...', 'warning');
    const res = await fetch('http://localhost:5000/api/admin/reports');
    const data = await res.json();
    
    document.getElementById('report-output-container').style.display = 'block';
    
    if (type === 'stats') {
        document.getElementById('report-title').innerText = "Enrolment Trends";
        document.getElementById('report-content').innerText = data.stats;
    } else if (type === 'workload') {
        document.getElementById('report-title').innerText = "Instructure Workload";
        document.getElementById('report-content').innerText = data.workload;
    } else if (type === 'popularity') {
        document.getElementById('report-title').innerText = "Course Popularity";
        document.getElementById('report-content').innerText = data.popularity;
    }
}


// --- UTILITIES ---

function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let icon = 'fa-circle-check';
    if (type === 'error') icon = 'fa-circle-xmark';
    if (type === 'warning') icon = 'fa-circle-exclamation';

    let title = type.charAt(0).toUpperCase() + type.slice(1);
    if (type === 'error') title = 'Error';

    toast.innerHTML = `
        <div class="toast-icon"><i class="fa-solid ${icon}"></i></div>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
    `;

    toastContainer.appendChild(toast);
    
    // Trigger animation
    setTimeout(() => toast.classList.add('show'), 10);

    // Remove toast after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}


// Start App
document.addEventListener('DOMContentLoaded', init);

async function showNotifications() {
    let uid = state.role === 'student' ? state.student.id : (state.role === 'instructure' ? state.instructure.id : 'admin');
    const res = await fetch(`${API_URL}/notifications/${uid}`);
    const notifs = await res.json();
    let msg = notifs.length ? notifs.map(n => `[${n.type}] ${JSON.stringify(n.payload)}`).join('\n') : "No notifications.";
    await uiAlert(msg);
}

async function submitDescRequest() {
    const courseId = document.getElementById('change-course-id').value;
    const desc = document.getElementById('change-desc').value;
    await fetch(`${API_URL}/instructure/change-desc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: state.instructure.id, course_id: courseId, desc: desc })
    });
    await uiAlert("Description Update Request Sent!");
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
    await uiAlert("Prerequisite Update Request Sent!");
    fetchState();
}

async function requestDescChange(courseId) {
    const desc = await uiPrompt("Enter new description:");
    if(!desc) return;
    await fetch(`${API_URL}/instructure/change-desc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: db.instructure.id, course_id: courseId, desc: desc })
    });
    await uiAlert("Description Update Request Sent!");
    fetchState();
}

async function requestPrereqChange(courseId) {
    const prereq = await uiPrompt("Enter prerequisite course ID:");
    if(!prereq) return;
    await fetch(`${API_URL}/instructure/change-prereq`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: db.instructure.id, course_id: courseId, prereq_id: prereq })
    });
    await uiAlert("Prerequisite Update Request Sent!");
    fetchState();
}

async function managePrograms() {
    const name = prompt("Enter new Degree Program Name:");
    if(!name) return;
    const id = prompt("Enter Program ID (e.g., CS-BS):");
    if(!id) return;
    
    await fetch(`${API_URL}/admin/programs`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id, name: name })
    });
    alert("Degree Program Created!");
    fetchState();
}

async function manageUsers() {
    const action = prompt("Type 'deactivate' to deactivate a user:");
    if(action !== 'deactivate') return;
    const uid = prompt("Enter User ID to deactivate:");
    if(!uid) return;
    
    await fetch(`${API_URL}/admin/users/deactivate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: uid })
    });
    alert("User Deactivated!");
    fetchState();
}

async function manageCourses() {
    const name = prompt("Enter new Course Name (e.g. Intro to Databases):");
    if(!name) return;
    const id = prompt("Enter Course ID (e.g. 6):");
    if(!id) return;
    const capacity = prompt("Enter Capacity:");
    if(!capacity) return;
    
    await fetch(`${API_URL}/admin/courses`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id, name: name, desc: name, instructor: 'Staff', capacity: parseInt(capacity), schedule: 'TBD' })
    });
    alert("Course Created!");
    fetchState();
}

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
    if(!id || !name) return await uiAlert("Fill fields");
    await fetch(`${API_URL}/admin/users/add`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name, role}) });
    await fetchState(); renderView();
}
async function editUserUI(id, oldName) {
    const name = await uiPrompt("Enter new name for " + id + ":", oldName);
    if(!name) return;
    await fetch(`${API_URL}/admin/users/edit`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name}) });
    await fetchState(); renderView();
}
async function deactivateUserUI(id) {
    if(!await uiConfirm("Deactivate " + id + "?")) return;
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
    if(!id || !name || !cap) return await uiAlert("Fill fields");
    await fetch(`${API_URL}/admin/courses`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name, desc: name, instructor: 'Staff', capacity: parseInt(cap), schedule: 'TBD'}) });
    await fetchState(); renderView();
}
async function editCourseUI(id, oldName) {
    const name = await uiPrompt("Enter new name for " + id + ":", oldName);
    const cap = await uiPrompt("Enter new capacity:");
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
    if(!id || !name) return await uiAlert("Fill fields");
    await fetch(`${API_URL}/admin/programs`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id, name}) });
    await fetchState(); renderView();
}
