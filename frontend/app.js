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
const notifBadge = document.getElementById('notif-badge');

// Navigation Config
const navConfig = {
    student: [
        { id: 'browse', icon: 'fa-book-open', label: 'Course Catalogue' },
        { id: 'schedule', icon: 'fa-calendar-days', label: 'My Schedule' },
        { id: 'progress', icon: 'fa-chart-line', label: 'Academic Progress' }
    ],
    faculty: [
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
    
    roleSelect.addEventListener('change', (e) => {
        currentRole = e.target.value;
        updateUserIdentity();
        renderNav();
        // Load default view for role
        currentView = navConfig[currentRole][0].id;
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
    } else if (currentRole === 'faculty') {
        userName.textContent = db.faculty.name;
        userId.textContent = `ID: ${db.faculty.id}`;
        userAvatar.textContent = db.faculty.name.charAt(0);
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
    } else if (currentRole === 'faculty') {
        if (currentView === 'my-classes') renderFacultyClasses();
        else if (currentView === 'roster') renderFacultyRoster();
        else if (currentView === 'grading') renderFacultyGrading();
    } else if (currentRole === 'admin') {
        if (currentView === 'dashboard') renderAdminDashboard();
        else if (currentView === 'courses') renderAdminCourses();
        else if (currentView === 'reports') renderAdminReports();
    }
}

// --- STUDENT VIEWS ---

function renderStudentBrowse() {
    const html = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Available Courses</h3>
            <div class="filters">
                <select class="form-control" style="width: auto;">
                    <option>All Departments</option>
                    <option>Computer Science</option>
                    <option>Mathematics</option>
                </select>
            </div>
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
            triggerNotification();
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
            triggerNotification();
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
            <td><button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;"><i class="fa-solid fa-video"></i> Join</button></td>
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

function renderStudentProgress() {
    viewContainer.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon"><i class="fa-solid fa-graduation-cap"></i></div>
                <div class="stat-info">
                    <h3>Credits Earned</h3>
                    <div class="stat-value">6 / 120</div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-icon"><i class="fa-solid fa-star"></i></div>
                <div class="stat-info">
                    <h3>Current GPA</h3>
                    <div class="stat-value">3.8</div>
                </div>
            </div>
        </div>

        <div class="mb-6">
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
                    <tr>
                        <td><strong>SCS1101</strong></td>
                        <td>Fall 2025</td>
                        <td><span class="status-badge status-success">A</span></td>
                        <td>3</td>
                    </tr>
                    <tr>
                        <td><strong>SCS2101</strong></td>
                        <td>Fall 2025</td>
                        <td><span class="status-badge status-success">A-</span></td>
                        <td>3</td>
                    </tr>
                </tbody>
            </table>
        </div>
    `;
}

// --- FACULTY VIEWS ---

function renderFacultyClasses() {
    const taughtCourses = db.courses.filter(c => db.faculty.taughtCourses.includes(c.id));
    
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
                
                <div style="display: flex; gap: 0.5rem;">
                    <button class="btn btn-primary" style="flex:1;" onclick="currentView='roster'; renderNav(); renderView();">View Roster</button>
                    <button class="btn btn-outline" style="flex:1;">Edit Details</button>
                </div>
            </div>
        `;
    });
    html += `</div>`;
    viewContainer.innerHTML = html;
}

function renderFacultyRoster() {
    let rows = db.students.map(s => `
        <tr>
            <td><strong>${s.id}</strong></td>
            <td>${s.name}</td>
            <td>${s.name.toLowerCase().replace(' ', '.')}@nexus.edu</td>
            <td><span class="status-badge status-success">Enrolled</span></td>
            <td><button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;">Message</button></td>
        </tr>
    `).join('');

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">SCS2303 - Class Roster</h3>
            <button class="btn btn-outline"><i class="fa-solid fa-download"></i> Export CSV</button>
        </div>
        <div class="data-table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Student ID</th>
                        <th>Name</th>
                        <th>Email</th>
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

function renderFacultyGrading() {
    let rows = db.students.map(s => `
        <tr>
            <td><strong>${s.id}</strong></td>
            <td>${s.name}</td>
            <td>
                <select class="form-control grade-select" style="width: 100px; padding: 0.5rem;">
                    <option value="">-</option>
                    <option value="A" ${s.grade === 'A' ? 'selected' : ''}>A</option>
                    <option value="B" ${s.grade === 'B' ? 'selected' : ''}>B</option>
                    <option value="C" ${s.grade === 'C' ? 'selected' : ''}>C</option>
                    <option value="F" ${s.grade === 'F' ? 'selected' : ''}>F</option>
                </select>
            </td>
            <td>Pending</td>
        </tr>
    `).join('');

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Grade Submission - SCS2303</h3>
            <button class="btn btn-primary" onclick="submitGrades()"><i class="fa-solid fa-check-double"></i> Submit All Grades</button>
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
                    </tr>
                </thead>
                <tbody>
                    ${rows}
                </tbody>
            </table>
        </div>
    `;
}

function submitGrades() {
    showToast('Validating grades...', 'warning');
    setTimeout(() => {
        showToast('Grades successfully submitted for approval.', 'success');
        triggerNotification();
    }, 1000);
}

// --- ADMIN VIEWS ---

function renderAdminDashboard() {
    const totalStudents = 12540;
    const totalCourses = db.courses.length;
    const sysLoad = '34%';

    viewContainer.innerHTML = `
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon" style="background-color: #E0E7FF; color: #4F46E5;"><i class="fa-solid fa-users"></i></div>
                <div class="stat-info">
                    <h3>Total Enrolled</h3>
                    <div class="stat-value">${totalStudents.toLocaleString()}</div>
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

        <div class="grid-cards" style="grid-template-columns: 2fr 1fr;">
            <div class="glass-card">
                <h3 class="section-title">Recent Activity</h3>
                <div class="data-table-container" style="box-shadow: none; border: none;">
                    <table class="data-table">
                        <tbody>
                            <tr>
                                <td><span class="status-badge status-success">Enrolment</span></td>
                                <td>Student 20261011 enrolled in SCS2303</td>
                                <td style="color: var(--text-muted); text-align: right;">Just now</td>
                            </tr>
                            <tr>
                                <td><span class="status-badge status-warning">Waitlist</span></td>
                                <td>Student 20269022 joined waitlist for SCS2301</td>
                                <td style="color: var(--text-muted); text-align: right;">5 mins ago</td>
                            </tr>
                            <tr>
                                <td><span class="status-badge" style="background-color: var(--primary-light); color: var(--primary);">System</span></td>
                                <td>Automated backup completed successfully</td>
                                <td style="color: var(--text-muted); text-align: right;">1 hour ago</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="glass-card">
                <h3 class="section-title">Alerts</h3>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <div style="padding: 1rem; border-left: 3px solid var(--danger); background-color: #FEF2F2; border-radius: 0 0.5rem 0.5rem 0;">
                        <h4 style="color: var(--danger); font-size: 0.875rem; margin-bottom: 0.25rem;">High Load Warning</h4>
                        <p style="font-size: 0.75rem; color: var(--text-muted);">Database connections exceeded 80% capacity.</p>
                    </div>
                    <div style="padding: 1rem; border-left: 3px solid var(--warning); background-color: #FEF3C7; border-radius: 0 0.5rem 0.5rem 0;">
                        <h4 style="color: var(--warning); font-size: 0.875rem; margin-bottom: 0.25rem;">Course Over Capacity</h4>
                        <p style="font-size: 0.75rem; color: var(--text-muted);">SCS2301 waitlist exceeds 20 students. Consider adding a section.</p>
                    </div>
                </div>
            </div>
        </div>
    `;
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
                <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;"><i class="fa-solid fa-pen"></i></button>
            </td>
        </tr>
    `}).join('');

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Course Catalogue Management</h3>
            <button class="btn btn-primary"><i class="fa-solid fa-plus"></i> Create Course</button>
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

function renderAdminReports() {
    viewContainer.innerHTML = `
        <div class="mb-6">
            <h3 class="section-title">Reporting & Analytics</h3>
        </div>
        <div class="grid-cards">
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-chart-line" style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Enrolment Trends</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); text-align: center; margin-bottom: 1.5rem;">Analyze enrolment data across departments and semesters.</p>
                <button class="btn btn-primary">Generate Report</button>
            </div>
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-user-graduate" style="font-size: 3rem; color: var(--accent); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Faculty Workload</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); text-align: center; margin-bottom: 1.5rem;">Review course assignments and credit hours per faculty.</p>
                <button class="btn btn-primary">Generate Report</button>
            </div>
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-fire" style="font-size: 3rem; color: var(--warning); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Course Popularity</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); text-align: center; margin-bottom: 1.5rem;">Identify high-demand courses for resource allocation.</p>
                <button class="btn btn-primary">Generate Report</button>
            </div>
        </div>
    `;
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

function triggerNotification() {
    const currentCount = parseInt(notifBadge.textContent) || 0;
    notifBadge.textContent = currentCount + 1;
    notifBadge.style.transform = 'scale(1.2)';
    setTimeout(() => {
        notifBadge.style.transform = 'scale(1)';
    }, 200);
}

// Start App
document.addEventListener('DOMContentLoaded', init);
