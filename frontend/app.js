
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

function uiPrompt(msg, defaultVal = '') {
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
        input.className = 'form-control';
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

function uiSelectPrompt(msg, options = []) {
    return new Promise(resolve => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;backdrop-filter:blur(4px);';
        const box = document.createElement('div');
        box.className = 'glass-card';
        box.style.cssText = 'background:var(--card-bg);padding:2rem;border-radius:1rem;min-width:300px;text-align:center;box-shadow:0 10px 25px rgba(0,0,0,0.2);';

        const text = document.createElement('div');
        text.style.marginBottom = '1rem';
        text.textContent = msg;

        const select = document.createElement('select');
        select.className = 'form-control';
        select.style.marginBottom = '1.5rem';
        select.style.width = '100%';
        
        options.forEach(opt => {
            const optionElement = document.createElement('option');
            optionElement.value = opt.value;
            optionElement.textContent = opt.label;
            select.appendChild(optionElement);
        });

        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'display:flex;gap:1rem;justify-content:center;';

        const yesBtn = document.createElement('button');
        yesBtn.className = 'btn btn-primary';
        yesBtn.textContent = 'Submit';
        yesBtn.onclick = () => { overlay.remove(); resolve(select.value); };

        const noBtn = document.createElement('button');
        noBtn.className = 'btn btn-secondary';
        noBtn.textContent = 'Cancel';
        noBtn.onclick = () => { overlay.remove(); resolve(null); };

        btnContainer.appendChild(yesBtn);
        btnContainer.appendChild(noBtn);
        box.appendChild(text);
        box.appendChild(select);
        box.appendChild(btnContainer);
        overlay.appendChild(box);
        document.body.appendChild(overlay);
        select.focus();
    });
}

function uiSchedulePrompt(msg) {
    return new Promise((resolve) => {
        const overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;';

        const box = document.createElement('div');
        box.style.cssText = 'background:var(--bg);padding:2rem;border-radius:1rem;box-shadow:0 10px 25px rgba(0,0,0,0.2);min-width:350px;font-family:inherit;';

        const text = document.createElement('div');
        text.style.marginBottom = '1rem';
        text.style.fontWeight = 'bold';
        text.textContent = msg;

        const daySelect = document.createElement('select');
        daySelect.className = 'form-control';
        daySelect.style.marginBottom = '1rem';
        ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].forEach(d => {
            let opt = document.createElement('option');
            opt.value = d; opt.textContent = d;
            daySelect.appendChild(opt);
        });

        const times = ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM"];
        
        const startSelect = document.createElement('select');
        startSelect.className = 'form-control';
        startSelect.style.marginBottom = '1rem';
        times.forEach(t => {
            let opt = document.createElement('option');
            opt.value = t; opt.textContent = t;
            startSelect.appendChild(opt);
        });

        const endSelect = document.createElement('select');
        endSelect.className = 'form-control';
        endSelect.style.marginBottom = '1.5rem';
        times.forEach(t => {
            let opt = document.createElement('option');
            opt.value = t; opt.textContent = t;
            endSelect.appendChild(opt);
        });

        const btnContainer = document.createElement('div');
        btnContainer.style.cssText = 'display:flex;gap:1rem;justify-content:center;';

        const yesBtn = document.createElement('button');
        yesBtn.className = 'btn btn-primary';
        yesBtn.textContent = 'Save Schedule';
        yesBtn.onclick = () => { 
            overlay.remove(); 
            resolve(`${daySelect.value} ${startSelect.value} - ${endSelect.value}`); 
        };

        const noBtn = document.createElement('button');
        noBtn.className = 'btn btn-secondary';
        noBtn.textContent = 'Cancel';
        noBtn.onclick = () => { overlay.remove(); resolve(null); };

        btnContainer.appendChild(yesBtn);
        btnContainer.appendChild(noBtn);
        
        box.appendChild(text);
        
        let l1 = document.createElement('label'); l1.textContent = "Day:"; l1.style.display="block"; l1.style.marginBottom="0.25rem";
        box.appendChild(l1);
        box.appendChild(daySelect);
        
        let l2 = document.createElement('label'); l2.textContent = "Start Time:"; l2.style.display="block"; l2.style.marginBottom="0.25rem";
        box.appendChild(l2);
        box.appendChild(startSelect);
        
        let l3 = document.createElement('label'); l3.textContent = "End Time:"; l3.style.display="block"; l3.style.marginBottom="0.25rem";
        box.appendChild(l3);
        box.appendChild(endSelect);
        
        box.appendChild(btnContainer);
        overlay.appendChild(box);
        document.body.appendChild(overlay);
    });
}

// API Configuration
const API_URL = 'http://localhost:5000/api';

// Data will be fetched from API
let db = {};
let currentUser = null;
let selectedInstructureCourseId = null;

async function fetchState() {
    try {
        const url = currentUser ? `${API_URL}/state?uid=${currentUser.id}` : `${API_URL}/state`;
        const res = await fetch(url);
        db = await res.json();
        
        if (currentUser) {
            const notifRes = await fetch(`${API_URL}/notifications/${currentUser.id}`);
            db.notifications = await notifRes.json();
        } else {
            db.notifications = [];
        }
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
        { id: 'reports', icon: 'fa-file-invoice', label: 'Reports & Analytics' },
        { id: 'assignments', icon: 'fa-wrench', label: 'Manual Assignments' },
        { id: 'admin_programs', icon: 'fa-graduation-cap', label: 'Degree Programs' }
    ]
};

// State
let currentRole = 'student';
let currentView = 'browse';

// Initialization
async function init() {
    await fetchState();

    // Check if we are already logged in
    if (!currentUser) {
        document.getElementById('login-container').style.display = 'flex';
        document.getElementById('app-container').style.display = 'none';
        updateLoginDropdown();
    } else {
        document.getElementById('login-container').style.display = 'none';
        document.getElementById('app-container').style.display = 'flex';
        updateUserIdentity();
        renderNav();
        renderView();
    }
}

function updateLoginDropdown() {
    const role = document.querySelector('input[name="loginRole"]:checked').value;
    const select = document.getElementById('login-user-select');
    select.innerHTML = '';

    let users = [];
    if (db && db.admin && db.admin.users) {
        users = db.admin.users.filter(u => (u.role || 'student') === role);
    }

    users.forEach(u => {
        const opt = document.createElement('option');
        opt.value = u.id;
        opt.textContent = `${u.id} - ${u.name}`;
        select.appendChild(opt);
    });
}

async function performLogin() {
    const role = document.querySelector('input[name="loginRole"]:checked').value;
    const select = document.getElementById('login-user-select');
    if (!select.value) return showToast("Please select a user", "error");

    const u = db.admin.users.find(x => x.id === select.value);
    if (!u) return;

    currentUser = u;
    currentRole = role;
    currentView = navConfig[currentRole][0].id;

    await fetchState(); // re-fetch with user context
    document.getElementById('login-container').style.display = 'none';
    document.getElementById('app-container').style.display = 'flex';

    updateUserIdentity();
    renderNav();
    renderView();
    showToast(`Logged in as ${u.name}`, 'success');
}



function performLogout() {
    currentUser = null;
    currentRole = 'student';
    currentView = 'browse';
    document.getElementById('app-container').style.display = 'none';
    document.getElementById('login-container').style.display = 'flex';
    updateLoginDropdown();
}


// User Identity
function updateUserIdentity() {
    if (currentRole === 'student' && db.student) {
        userName.textContent = db.student.name;
        userId.textContent = `ID: ${db.student.id}`;
        userAvatar.textContent = db.student.name.charAt(0);
    } else if (currentRole === 'instructure' && db.instructure) {
        userName.textContent = db.instructure.name;
        userId.textContent = `ID: ${db.instructure.id}`;
        userAvatar.textContent = db.instructure.name.charAt(0);
    } else {
        userName.textContent = currentUser ? currentUser.name : 'System Admin';
        userId.textContent = currentUser ? `ID: ${currentUser.id}` : 'ID: ADMIN-01';
        userAvatar.textContent = currentUser ? currentUser.name.charAt(0) : 'A';
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
        else if (currentView === 'assignments') renderAdminManualAssignments();
    }
}

// --- STUDENT VIEWS ---

function renderStudentBrowse() {
    const depts = [...new Set(db.courses.map(c => c.department).filter(Boolean))];
    const insts = [...new Set(db.courses.map(c => c.instructor).filter(Boolean))];
    
    let deptOptions = '<option value="">All Departments</option>';
    depts.forEach(d => deptOptions += `<option value="${d}">${d}</option>`);
    
    let instOptions = '<option value="">All Instructors</option>';
    insts.forEach(i => instOptions += `<option value="${i}">${i}</option>`);

    const html = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Available Courses</h3>
        </div>
        
        <div class="glass-card mb-6" style="padding: 1.5rem; display: flex; flex-wrap: wrap; gap: 1rem; align-items: end;">
            <div class="form-group mb-0" style="flex: 1; min-width: 200px;">
                <label class="form-label">Search Keyword</label>
                <input type="text" id="search-keyword" placeholder="Course Code or Keyword..." class="form-control">
            </div>
            <div class="form-group mb-0">
                <label class="form-label">Department</label>
                <select id="search-dept" class="form-control" style="width: 180px;">
                    ${deptOptions}
                </select>
            </div>
            <div class="form-group mb-0">
                <label class="form-label">Instructor</label>
                <select id="search-inst" class="form-control" style="width: 180px;">
                    ${instOptions}
                </select>
            </div>
            <button class="btn btn-primary" onclick="performCourseSearch()" style="margin-bottom: 0;"><i class="fa-solid fa-search"></i> Search</button>
            <button class="btn btn-secondary" onclick="clearCourseSearch()" style="margin-bottom: 0;"><i class="fa-solid fa-xmark"></i> Clear</button>
        </div>
        
        <div class="grid-cards" id="course-grid"></div>
    `;
    viewContainer.innerHTML = html;

    renderCourseGrid(db.courses);
}

function renderCourseGrid(coursesList) {
    const grid = document.getElementById('course-grid');
    grid.innerHTML = '';
    
    if (!coursesList || coursesList.length === 0) {
        grid.innerHTML = '<p style="color: var(--text-muted); text-align: center; width: 100%; grid-column: 1 / -1;">No courses found matching your criteria.</p>';
        return;
    }

    coursesList.forEach(course => {
        const isEnrolled = db.student.enrolledCourses.includes(course.id);
        const isFull = course.enrolled >= course.capacity;

        let actionBtn = `<button class="btn btn-primary" onclick="enrolCourse('${course.id}')">Enrol Now</button>`;
        if (isEnrolled) {
            actionBtn = `<button class="btn btn-danger" onclick="dropCourse('${course.id}')">Drop Course</button>`;
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
                    <div class="meta-item"><i class="fa-solid fa-building"></i> ${course.department || 'N/A'}</div>
                    <div class="meta-item"><i class="fa-solid fa-user-tie"></i> ${course.instructor}</div>
                    <div class="meta-item"><i class="fa-solid fa-clock"></i> ${course.schedule}</div>
                    <div class="meta-item"><i class="fa-solid fa-award"></i> ${course.credits} Credits</div>
                    <div class="meta-item" style="width: 100%;"><i class="fa-solid fa-book"></i> Prereqs: ${course.prerequisites && course.prerequisites.length ? course.prerequisites.join(', ') : 'None'}</div>
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

function clearCourseSearch() {
    document.getElementById('search-keyword').value = '';
    document.getElementById('search-dept').value = '';
    document.getElementById('search-inst').value = '';
    renderCourseGrid(db.courses);
}

async function performCourseSearch() {
    const q = document.getElementById('search-keyword').value;
    const dept = document.getElementById('search-dept').value;
    const instructor = document.getElementById('search-inst').value;
    
    showToast('Searching courses...', 'warning');
    
    try {
        const queryParams = new URLSearchParams({ q, dept, instructor });
        const res = await fetch(`${API_URL}/courses/search?${queryParams.toString()}`);
        const data = await res.json();
        
        if (data.status === 'success') {
            renderCourseGrid(data.courses);
        } else {
            showToast('Search failed.', 'error');
        }
    } catch (e) {
        showToast('API error during search.', 'error');
    }
}

async function enrolCourse(courseId) {
    showToast('Processing enrolment transaction via Python Core...', 'warning');

    try {
        const res = await fetch('http://localhost:5000/api/enroll', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
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
            headers: { 'Content-Type': 'application/json' },
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

let currentScheduleDate = new Date();

function changeScheduleWeek(offsetDays) {
    currentScheduleDate.setDate(currentScheduleDate.getDate() + offsetDays);
    renderView();
}

function getActiveSchedule(course, targetDate) {
    if (!course.schedule_history || course.schedule_history.length === 0) return course.schedule;
    let active = course.schedule_history[0].schedule;
    for (let i = 0; i < course.schedule_history.length; i++) {
        let entryDate = new Date(course.schedule_history[i].effective_date);
        if (entryDate <= targetDate) {
            active = course.schedule_history[i].schedule;
        }
    }
    return active;
}

function parseScheduleStr(schedStr) {
    try {
        const parts = schedStr.split(' ');
        return { day: parts[0], timeStr: parts.slice(1).join(' ') };
    } catch(e) { return { day: '', timeStr: schedStr }; }
}

function renderStudentSchedule() {
    const enrolledCourses = db.courses.filter(c => db.student.enrolledCourses.includes(c.id));

    let startOfWeek = new Date(currentScheduleDate);
    const dayOfWeek = startOfWeek.getDay();
    const diff = startOfWeek.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1);
    startOfWeek.setDate(diff);
    startOfWeek.setHours(0,0,0,0);
    
    let endOfWeek = new Date(startOfWeek);
    endOfWeek.setDate(startOfWeek.getDate() + 6);
    
    let headerHtml = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">My Schedule</h3>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <button class="btn btn-outline" onclick="changeScheduleWeek(-7)"><i class="fa-solid fa-chevron-left"></i> Prev</button>
                <span style="font-weight: 600;">${startOfWeek.toDateString()} - ${endOfWeek.toDateString()}</span>
                <button class="btn btn-outline" onclick="changeScheduleWeek(7)">Next <i class="fa-solid fa-chevron-right"></i></button>
            </div>
        </div>
    `;

    if (enrolledCourses.length === 0) {
        viewContainer.innerHTML = headerHtml + `
            <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
                <i class="fa-regular fa-calendar-xmark" style="font-size: 4rem; color: var(--text-light); margin-bottom: 1rem;"></i>
                <h3 style="color: var(--text-muted);">No courses scheduled</h3>
                <p style="color: var(--text-light); margin-top: 0.5rem; margin-bottom: 1.5rem;">You haven't enrolled in any courses for this semester.</p>
                <button class="btn btn-primary" onclick="currentView='browse'; renderNav(); renderView();">Browse Courses</button>
            </div>
        `;
        return;
    }

    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    let calendarHtml = `<div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 1rem; margin-top: 2rem;">`;
    
    for (let i = 0; i < 7; i++) {
        let currentDayDate = new Date(startOfWeek);
        currentDayDate.setDate(startOfWeek.getDate() + i);
        currentDayDate.setHours(23, 59, 59, 999);
        
        let dayStr = days[i];
        
        calendarHtml += `
            <div class="glass-card" style="padding: 1rem; min-height: 300px; display: flex; flex-direction: column; gap: 0.5rem;">
                <h4 style="text-align: center; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 0.5rem;">${dayStr} <br><small style="font-weight: normal; color: var(--text-light);">${currentDayDate.getDate()}/${currentDayDate.getMonth()+1}</small></h4>
        `;
        
        enrolledCourses.forEach(course => {
            const activeSched = getActiveSchedule(course, currentDayDate);
            const parsed = parseScheduleStr(activeSched);
            if (parsed.day.includes(dayStr)) {
                calendarHtml += `
                    <div style="background-color: var(--primary-light); border-left: 4px solid var(--primary); padding: 0.5rem; border-radius: 4px; font-size: 0.85rem;">
                        <strong>${course.code}</strong><br>
                        ${parsed.timeStr}<br>
                        <small>${course.instructor}</small>
                    </div>
                `;
            }
        });
        
        calendarHtml += `</div>`;
    }
    
    calendarHtml += `</div>`;
    viewContainer.innerHTML = headerHtml + calendarHtml;
}

function renderStudentProgress() {
    const gradePoints = { 'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0 };
    let totalPoints = 0;
    
    // Get program details
    let programName = "Undeclared Program";
    let requiredCredits = 120;
    let requiredCourses = [];
    if (db.admin && db.admin.programs && db.student.program_id) {
        const prog = db.admin.programs.find(p => p.id === db.student.program_id);
        if (prog) {
            programName = prog.name;
            requiredCredits = prog.required_credits || 120;
            requiredCourses = prog.required_courses || [];
        }
    }

    const completedIds = db.student.completedCourses.map(c => c.id);
    const creditsEarned = db.student.completedCourses.length * 3;
    const progressPercent = Math.min(100, Math.round((creditsEarned / requiredCredits) * 100));

    let completedCards = db.student.completedCourses.map(c => {
        totalPoints += gradePoints[c.grade] || 4.0;
        return `
            <div class="glass-card" style="padding: 1rem; border-left: 4px solid var(--accent); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin-bottom: 0.25rem;">${c.id}</h4>
                    <span style="font-size: 0.875rem; color: var(--text-muted);">Credits: 3</span>
                </div>
                <div style="text-align: right;">
                    <span class="status-badge status-success" style="font-size: 1rem; padding: 0.5rem 1rem;">Grade: ${c.grade}</span>
                </div>
            </div>
        `;
    }).join('');
    
    if (db.student.completedCourses.length === 0) {
        completedCards = `<div class="glass-card" style="padding: 2rem; text-align: center; color: var(--text-muted);">No courses completed yet.</div>`;
    }

    const stillRequiredIds = requiredCourses.filter(cId => !completedIds.includes(cId));
    let requiredCards = stillRequiredIds.map(cId => {
        // Find course name if available in db.courses
        const courseInfo = db.courses.find(c => c.id === cId || c.code === cId);
        const courseName = courseInfo ? courseInfo.title : "Core Requirement";
        return `
            <div class="glass-card" style="padding: 1rem; border-left: 4px solid var(--warning); display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin-bottom: 0.25rem;">${cId}</h4>
                    <span style="font-size: 0.875rem; color: var(--text-muted);">${courseName}</span>
                </div>
                <div>
                    <span class="status-badge status-warning">Pending</span>
                </div>
            </div>
        `;
    }).join('');
    
    if (stillRequiredIds.length === 0 && requiredCourses.length > 0) {
        requiredCards = `<div class="glass-card" style="padding: 2rem; text-align: center; color: var(--accent); border: 1px solid var(--accent);"><i class="fa-solid fa-check-circle"></i> All requirements fulfilled!</div>`;
    } else if (requiredCourses.length === 0) {
        requiredCards = `<div class="glass-card" style="padding: 2rem; text-align: center; color: var(--text-muted);">No specific course requirements defined for this program.</div>`;
    }

    const gpa = db.student.completedCourses.length ? (totalPoints / db.student.completedCourses.length).toFixed(1) : '0.0';

    viewContainer.innerHTML = `
        <div class="glass-card mb-6" style="padding: 2rem; background: linear-gradient(135deg, rgba(79, 70, 229, 0.1), rgba(255, 255, 255, 0.5)); border: 1px solid rgba(79, 70, 229, 0.2);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h2 style="color: var(--secondary); margin-bottom: 0.25rem;"><i class="fa-solid fa-graduation-cap" style="color: var(--primary);"></i> ${programName}</h2>
                    <p style="color: var(--text-muted);">Academic Progress Report</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 2rem; font-weight: 700; color: var(--primary);">${gpa}</div>
                    <div style="font-size: 0.875rem; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">Cumulative GPA</div>
                </div>
            </div>
            
            <div class="progress-container mb-6">
                <div class="progress-header" style="font-weight: 600;">
                    <span>Degree Progress</span>
                    <span>${creditsEarned} / ${requiredCredits} Credits (${progressPercent}%)</span>
                </div>
                <div class="progress-bar" style="height: 12px; background-color: rgba(0,0,0,0.05);">
                    <div class="progress-fill" style="width: ${progressPercent}%; background: linear-gradient(90deg, var(--primary), var(--accent));"></div>
                </div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
            <!-- Completed Section -->
            <div>
                <h3 class="section-title" style="display: flex; align-items: center; gap: 0.5rem;"><i class="fa-solid fa-check-circle" style="color: var(--accent);"></i> Completed Courses</h3>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    ${completedCards}
                </div>
            </div>
            
            <!-- Required Section -->
            <div>
                <h3 class="section-title" style="display: flex; align-items: center; gap: 0.5rem;"><i class="fa-solid fa-hourglass-half" style="color: var(--warning);"></i> Still Required</h3>
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    ${requiredCards}
                </div>
            </div>
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
                        <span>${Math.round((course.enrolled / course.capacity) * 100)}%</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${(course.enrolled / course.capacity) * 100}%"></div>
                    </div>
                </div>
                
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <button class="btn btn-primary" style="flex:1; min-width: 120px;" onclick="selectedInstructureCourseId='${course.id}'; currentView='roster'; renderNav(); renderView();">View Roster</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestCapacityChange('${course.id}')">Req Capacity</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestDescChange('${course.id}')">Req Desc Change</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestPrereqChange('${course.id}')">Add Prerequisite</button>
                    <button class="btn btn-outline" style="flex:1; min-width: 120px;" onclick="requestScheduleChange('${course.id}')">Change Schedule</button>
                </div>
            </div>
        `;
    });
    html += `</div>`;
    viewContainer.innerHTML = html;
}

function renderInstructureRoster() {
    if (!db.instructure.taughtCourses || db.instructure.taughtCourses.length === 0) {
        viewContainer.innerHTML = '<p style="padding:2rem;text-align:center;">No courses assigned.</p>';
        return;
    }
    
    let instructureCourseId = selectedInstructureCourseId;
    if (!instructureCourseId || !db.instructure.taughtCourses.includes(instructureCourseId)) {
        instructureCourseId = db.instructure.taughtCourses[0];
    }
    selectedInstructureCourseId = instructureCourseId; // persist
    
    const courseObj = db.courses.find(c => c.id == instructureCourseId);
    const courseTitle = courseObj ? courseObj.code : instructureCourseId;
    
    let courseSelector = `<select class="form-control" onchange="selectedInstructureCourseId=this.value; renderView()" style="width: 250px; font-weight: bold;">`;
    db.instructure.taughtCourses.forEach(cid => {
        const c = db.courses.find(c => c.id == cid);
        courseSelector += `<option value="${cid}" ${cid === instructureCourseId ? 'selected' : ''}>${c ? c.code + ' - ' + c.title : cid}</option>`;
    });
    courseSelector += `</select>`;
    
    const enrolledStudents = db.students.filter(s => s.enrolledCourses && s.enrolledCourses.includes(String(instructureCourseId)));

    let rows = enrolledStudents.map(s => `
        <tr>
            <td><strong>${s.id}</strong></td>
            <td>${s.name}</td>
            <td>${s.name.toLowerCase().replace(' ', '.')}@nexus.edu</td>
            <td><span class="status-badge status-success">Enrolled</span></td>
        </tr>
    `).join('');
    
    if (!rows) {
        rows = '<tr><td colspan="4" style="text-align: center; color: var(--text-muted); padding: 2rem;">No students currently enrolled.</td></tr>';
    }

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Class Roster</h3>
            ${courseSelector}
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
    if (!db.instructure.taughtCourses || db.instructure.taughtCourses.length === 0) {
        viewContainer.innerHTML = '<p style="padding:2rem;text-align:center;">No courses assigned.</p>';
        return;
    }

    let instructureCourseId = selectedInstructureCourseId;
    if (!instructureCourseId || !db.instructure.taughtCourses.includes(instructureCourseId)) {
        instructureCourseId = db.instructure.taughtCourses[0];
    }
    selectedInstructureCourseId = instructureCourseId;

    const courseObj = db.courses.find(c => c.id == instructureCourseId);
    const courseTitle = courseObj ? courseObj.code : instructureCourseId;
    
    let courseSelector = `<select class="form-control" onchange="selectedInstructureCourseId=this.value; renderView()" style="width: 250px; font-weight: bold;">`;
    db.instructure.taughtCourses.forEach(cid => {
        const c = db.courses.find(c => c.id == cid);
        courseSelector += `<option value="${cid}" ${cid === instructureCourseId ? 'selected' : ''}>${c ? c.code + ' - ' + c.title : cid}</option>`;
    });
    courseSelector += `</select>`;

    const pendingStudentIds = (db.admin && db.admin.pending_grades)
        ? db.admin.pending_grades.filter(g => String(g.course_id) == String(instructureCourseId)).map(g => String(g.student_id))
        : [];
        
    const enrolledStudents = db.students.filter(s => s.enrolledCourses && s.enrolledCourses.includes(String(instructureCourseId)));

    let rows = enrolledStudents.map(s => {
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
    
    if (!rows) {
        rows = '<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 2rem;">No students currently enrolled.</td></tr>';
    }

    viewContainer.innerHTML = `
        <div class="mb-6 flex-between">
            <h3 class="section-title">Grade Submission</h3>
            ${courseSelector}
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
        
        <div style="margin-top: 1rem; text-align: right;">
            <button class="btn btn-primary" onclick="submitBatchGrades('${instructureCourseId}')">Submit All Grades</button>
        </div>
    `;
}

async function submitBatchGrades(courseId) {
    const grades = [];
    const selects = document.querySelectorAll('.grade-select');
    selects.forEach(sel => {
        if (sel.value) {
            grades.push({
                student_id: sel.id.replace('grade-sel-', ''),
                grade: sel.value
            });
        }
    });
    
    if (grades.length === 0) {
        showToast('No grades selected.', 'warning');
        return;
    }
    
    showToast('Submitting batch grades...', 'warning');
    const res = await fetch(`${API_URL}/instructure/grades/submit_batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ course_id: courseId, instructure_id: db.instructure.id, grades: grades })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

async function submitSingleGrade(studentId, courseId) {
    showToast('Validating grade via State Pattern...', 'warning');

    const gradeSelect = document.getElementById('grade-sel-' + studentId);
    const grade = gradeSelect ? gradeSelect.value : '';

    const res = await fetch('http://localhost:5000/api/instructure/grades/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ course_id: courseId, instructure_id: db.instructure.id, capacity: newCap })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

async function requestScheduleChange(courseId) {
    const newSchedule = await uiSchedulePrompt("Change Schedule for " + courseId);
    if (!newSchedule) return;

    showToast('Sending Course Change Request Command...', 'warning');

    const res = await fetch('http://localhost:5000/api/instructure/change-schedule', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ course_id: courseId, instructure_id: db.instructure.id, schedule: newSchedule })
    });
    const data = await res.json();
    showToast('State Pattern Processed: ' + data.status, data.status);
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, title, instructor, capacity })
    });
    const data = await res.json();
    showToast(data.message, data.status);
    await fetchState();
    renderView();
}

async function editCourse(courseId) {
    const c = db.courses.find(x => x.id === courseId) || db.admin.courses.find(x => x.id === courseId);
    if (!c) return;
    openEditModal(c);
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
        
        </div>
        
        <div class="glass-card mb-6" style="margin-top: 2rem;">
            <h3 class="section-title">High-Capacity Report</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; align-items: end; margin-top: 1rem;">
                <div class="form-group mb-0">
                    <label class="form-label">Department</label>
                    <input type="text" id="report-dept" class="form-control" placeholder="e.g. CS">
                </div>
                <div class="form-group mb-0">
                    <label class="form-label">Threshold %</label>
                    <input type="number" id="report-thresh" class="form-control" placeholder="e.g. 90">
                </div>
                <button class="btn btn-primary" onclick="generateHighCapacityReport()" style="margin-bottom: 1rem;">Generate</button>
            </div>
        </div>

        <div id="report-output-container" class="glass-card" style="margin-top: 2rem; display: none;">
            <h3 class="section-title" id="report-title">Report Title</h3>
            <pre id="report-content" style="background: var(--bg-color); padding: 1.5rem; border-radius: 0.5rem; white-space: pre-wrap; font-family: monospace; border-left: 4px solid var(--primary);"></pre>
        </div>
    `;
}

async function generateHighCapacityReport() {
    const dept = document.getElementById('report-dept').value;
    const thresh = document.getElementById('report-thresh').value;
    if (!dept || !thresh) return await uiAlert("Fill all fields");

    document.getElementById('report-output-container').style.display = 'block';
    document.getElementById('report-title').textContent = "High-Capacity Report";
    document.getElementById('report-content').textContent = "Generating...";

    try {
        const res = await fetch(`${API_URL}/admin/reports/high_capacity`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ department: dept, threshold: thresh })
        });
        const data = await res.json();
        if (data.status === 'success') {
            document.getElementById('report-content').textContent = data.content;
        } else {
            document.getElementById('report-content').textContent = "Failed to generate report.";
        }
    } catch (e) {
        document.getElementById('report-content').textContent = "Error: " + e;
    }
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
    if (!currentUser) return;
    const res = await fetch(`${API_URL}/notifications/${currentUser.id}`);
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
    if (!desc) return;
    await fetch(`${API_URL}/instructure/change-desc`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ instructure_id: db.instructure.id, course_id: courseId, desc: desc })
    });
    await uiAlert("Description Update Request Sent!");
    fetchState();
}

async function requestPrereqChange(courseId) {
    const options = db.courses
        .filter(c => c.id !== courseId)
        .map(c => ({ value: c.id, label: `${c.code} - ${c.title}` }));
        
    const prereq = await uiSelectPrompt("Select prerequisite course:", options);
    if (!prereq) return;
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
    if (!name) return;
    const id = prompt("Enter Program ID (e.g., CS-BS):");
    if (!id) return;

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
    if (action !== 'deactivate') return;
    const uid = prompt("Enter User ID to deactivate:");
    if (!uid) return;

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
    if (!name) return;
    const id = prompt("Enter Course ID (e.g. 6):");
    if (!id) return;
    const capacity = prompt("Enter Capacity:");
    if (!capacity) return;

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
            <td><span class="status-badge" style="background:var(--secondary);color:white;">${u.role || 'Unknown'}</span></td>
            <td>${u.name}</td>
            <td>${u.email || u.id + '@nexus.edu'}</td>
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
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div class="form-group"><label class="form-label">User ID</label><input type="text" id="add-uid" class="form-control" placeholder="User ID"></div>
                <div class="form-group"><label class="form-label">Full Name</label><input type="text" id="add-uname" class="form-control" placeholder="Full Name"></div>
                <div class="form-group"><label class="form-label">Email</label><input type="email" id="add-uemail" class="form-control" placeholder="Email"></div>
                <div class="form-group">
                    <label class="form-label">Role</label>
                    <select id="add-urole" class="form-control"><option value="student">Student</option><option value="instructure">Instructure</option></select>
                </div>
            </div>
            <button class="btn btn-primary" onclick="addUserUI()" style="margin-top:1rem; width:100%;">Create User</button>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <thead><tr><th>ID</th><th>Role</th><th>Name</th><th>Email</th><th>Status</th><th>Actions</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        </div>

    `;
}

function renderAdminManualAssignments() {
    viewContainer.innerHTML = `
        <div class="glass-card mb-6" style="max-width: 800px; margin: 0 auto; margin-top: 2rem;">
            
            <h3 class="section-title">Manual Override: Force-Add Student to Course</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; align-items: end; margin-bottom: 2rem;">
                <div class="form-group mb-0">
                    <label class="form-label">Student ID</label>
                    <input type="text" id="force-sid" class="form-control" placeholder="Student ID">
                </div>
                <div class="form-group mb-0">
                    <label class="form-label">Course ID</label>
                    <input type="text" id="force-cid" class="form-control" placeholder="Course ID">
                </div>
                <button class="btn btn-warning" onclick="forceAddUI()" style="margin-bottom: 1rem;">Force-Add</button>
            </div>
            
            <h3 class="section-title">Assign Course to Instructor</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 1rem; align-items: end;">
                <div class="form-group mb-0">
                    <label class="form-label">Faculty ID</label>
                    <input type="text" id="assign-fid" class="form-control" placeholder="Faculty ID">
                </div>
                <div class="form-group mb-0">
                    <label class="form-label">Course ID</label>
                    <input type="text" id="assign-cid" class="form-control" placeholder="Course ID">
                </div>
                <button class="btn btn-primary" onclick="assignCourseUI()" style="margin-bottom: 1rem;">Assign</button>
            </div>
            
        </div>
    `;
}

async function addUserUI() {
    const id = document.getElementById('add-uid').value;
    const name = document.getElementById('add-uname').value;
    const email = document.getElementById('add-uemail').value;
    const role = document.getElementById('add-urole').value;
    if (!id || !name) return await uiAlert("Fill fields");
    await fetch(`${API_URL}/admin/users/add`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, name, role, email }) });
    await fetchState(); renderView();
}
async function editUserUI(id) {
    const u = db.admin.users.find(x => x.id === id);
    if (!u) return;
    openEditUserModal(u);
}

function openEditUserModal(u) {
    const existing = document.getElementById('edit-user-modal');
    if (existing) existing.remove();
    const modalHtml = `
    <div id="edit-user-modal" class="login-container" style="z-index: 10000; display: flex;">
        <div class="login-card" style="max-width: 500px; width: 100%;">
            <h3 style="margin-bottom: 1rem; color: var(--primary);">Edit User: ${u.id}</h3>
            <div style="display: grid; grid-template-columns: 1fr; gap: 1rem;">
                <div class="form-group mb-0"><label class="form-label">Name</label><input type="text" id="edit-uname" class="form-control" value="${u.name || ''}"></div>
                <div class="form-group mb-0"><label class="form-label">Email</label><input type="email" id="edit-uemail" class="form-control" value="${u.email || ''}"></div>
                <div style="color: var(--text-muted); font-size: 0.875rem;">Role cannot be modified (current: <strong>${u.role}</strong>)</div>
            </div>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <button class="btn btn-outline" style="flex: 1;" onclick="document.getElementById('edit-user-modal').remove()">Cancel</button>
                <button class="btn btn-primary" style="flex: 1;" onclick="submitEditUser('${u.id}', '${u.role}')">Save Changes</button>
            </div>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function submitEditUser(id, role) {
    const payload = {
        id,
        name: document.getElementById('edit-uname').value,
        email: document.getElementById('edit-uemail').value,
        role
    };
    showToast('Editing user...', 'warning');
    const res = await fetch(`${API_URL}/admin/users/edit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await res.json();
    showToast(data.message || 'User updated', data.status || 'success');
    document.getElementById('edit-user-modal').remove();
    await fetchState();
    renderView();
}
async function deactivateUserUI(id) {
    if (!await uiConfirm("Deactivate " + id + "?")) return;
    await fetch(`${API_URL}/admin/users/deactivate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id }) });
    await fetchState(); renderView();
}

async function forceAddUI() {
    const sid = document.getElementById('force-sid').value;
    const cid = document.getElementById('force-cid').value;
    if (!sid || !cid) return await uiAlert("Fill fields");
    const res = await fetch(`${API_URL}/admin/force_add`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ student_id: sid, course_id: cid }) });
    if (res.ok) { await uiAlert("Student forced into course successfully."); await fetchState(); }
    else { await uiAlert("Force-Add Failed."); }
}

async function assignCourseUI() {
    const fid = document.getElementById('assign-fid').value;
    const cid = document.getElementById('assign-cid').value;
    if (!fid || !cid) return await uiAlert("Fill fields");
    const res = await fetch(`${API_URL}/admin/assign_course`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ instructure_id: fid, course_id: cid }) });
    if (res.ok) { await uiAlert("Course assigned successfully."); await fetchState(); }
    else { await uiAlert("Course Assignment Failed."); }
}

function renderAdminCoursesCRUD() {
    let rows = db.admin.courses.map(c => `
        <tr>
            <td>${c.id}</td>
            <td>${c.name}</td>
            <td>${c.department || 'N/A'}</td>
            <td>${c.instructor || 'Staff'}</td>
            <td>${c.enrolled_count !== undefined ? c.enrolled_count : 0}/${c.capacity}</td>
            <td>
                <button class="btn btn-outline" style="padding: 0.25rem 0.5rem; font-size: 0.75rem;" onclick="editCourseUI('${c.id}', '${c.name}')">Edit</button>
            </td>
        </tr>
    `).join('');

    const depts = [...new Set(db.admin.courses.map(c => c.department).filter(Boolean))];
    const instructors = db.admin.users.filter(u => u.role === 'instructure');
    
    let deptOptions = '<option value="">Select Department</option>';
    depts.forEach(d => deptOptions += `<option value="${d}">${d}</option>`);
    
    let instOptions = '<option value="">Select Instructor</option>';
    instructors.forEach(u => instOptions += `<option value="${u.id}">${u.name} (${u.id})</option>`);

    viewContainer.innerHTML = `
        <div class="mb-6" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="section-title">Manage Courses</h3>
            <button class="btn btn-secondary" onclick="currentView='dashboard'; renderNav(); renderView();">Back to Dashboard</button>
        </div>
        
        <div class="glass-card mb-6">
            <h3>Add New Course</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div class="form-group"><label class="form-label">Course ID</label><input type="text" id="add-cid" class="form-control" placeholder="e.g. CS101"></div>
                <div class="form-group"><label class="form-label">Course Name</label><input type="text" id="add-cname" class="form-control" placeholder="Course Name"></div>
                <div class="form-group">
                    <label class="form-label">Department</label>
                    <select id="add-cdept" class="form-control">
                        ${deptOptions}
                    </select>
                </div>
                <div class="form-group">
                    <label class="form-label">Instructor</label>
                    <select id="add-cinstructor" class="form-control">
                        ${instOptions}
                    </select>
                </div>
                <div class="form-group"><label class="form-label">Capacity</label><input type="number" id="add-ccap" class="form-control" placeholder="Capacity"></div>
                <div class="form-group"><label class="form-label">Days</label><input type="text" id="add-cdays" class="form-control" placeholder="e.g. MO,WE"></div>
                <div class="form-group"><label class="form-label">Start Time</label><input type="time" id="add-cstart" class="form-control" placeholder="Start (HH:MM)"></div>
                <div class="form-group"><label class="form-label">End Time</label><input type="time" id="add-cend" class="form-control" placeholder="End (HH:MM)"></div>
                <div class="form-group" style="grid-column: span 2;"><label class="form-label">Prerequisites</label><input type="text" id="add-cprereq" class="form-control" placeholder="Prerequisites (comma-sep)"></div>
            </div>
            <button class="btn btn-primary" onclick="addCourseUI()" style="margin-top: 1rem; width: 100%;">Create Course</button>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <thead><tr><th>ID</th><th>Name</th><th>Dept</th><th>Instructor</th><th>Seats</th><th>Actions</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}

async function addCourseUI() {
    const id = document.getElementById('add-cid').value;
    const name = document.getElementById('add-cname').value;
    const dept = document.getElementById('add-cdept').value;
    const instructor = document.getElementById('add-cinstructor').value;
    const cap = document.getElementById('add-ccap').value;
    const days = document.getElementById('add-cdays').value;
    const start = document.getElementById('add-cstart').value;
    const end = document.getElementById('add-cend').value;
    const prereq = document.getElementById('add-cprereq').value;

    if (!id || !name || !cap || !dept || !instructor) return await uiAlert("Fill all required fields");
    const payload = {
        id, name, desc: name, capacity: parseInt(cap),
        instructor, department: dept, days, start_time: start, end_time: end, prerequisites: prereq
    };
    await fetch(`${API_URL}/admin/courses`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
    await fetchState(); renderView();
}
async function editCourseUI(id, oldName) {
    const c = db.courses.find(x => x.id === id) || db.admin.courses.find(x => x.id === id);
    if (!c) return;
    openEditModal(c);
}

function openEditModal(c) {
    const existing = document.getElementById('edit-modal');
    if (existing) existing.remove();
    const modalHtml = `
    <div id="edit-modal" class="login-container" style="z-index: 10000; display: flex;">
        <div class="login-card" style="max-width: 500px; width: 100%;">
            <h3 style="margin-bottom: 1rem; color: var(--primary);">Edit Course: ${c.id}</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div class="form-group mb-0"><label class="form-label">Name / Code</label><input type="text" id="edit-cname" class="form-control" value="${c.code || c.name || ''}"></div>
                <div class="form-group mb-0"><label class="form-label">Department</label><input type="text" id="edit-cdept" class="form-control" value="${c.department || ''}"></div>
                <div class="form-group mb-0" style="grid-column: span 2;"><label class="form-label">Title / Description</label><input type="text" id="edit-ctitle" class="form-control" value="${c.title || c.desc || ''}"></div>
                <div class="form-group mb-0"><label class="form-label">Instructor</label><input type="text" id="edit-cinstructor" class="form-control" value="${c.instructor || ''}"></div>
                <div class="form-group mb-0"><label class="form-label">Capacity</label><input type="number" id="edit-ccap" class="form-control" value="${c.capacity || 0}"></div>
                <div class="form-group mb-0"><label class="form-label">Start Time</label><input type="time" id="edit-cstart" class="form-control" value="${c.start_time || ''}"></div>
                <div class="form-group mb-0"><label class="form-label">End Time</label><input type="time" id="edit-cend" class="form-control" value="${c.end_time || ''}"></div>
            </div>
            <div style="display: flex; gap: 1rem; margin-top: 1.5rem;">
                <button class="btn btn-outline" style="flex: 1;" onclick="document.getElementById('edit-modal').remove()">Cancel</button>
                <button class="btn btn-primary" style="flex: 1;" onclick="submitEditCourse('${c.id}')">Save Changes</button>
            </div>
        </div>
    </div>`;
    document.body.insertAdjacentHTML('beforeend', modalHtml);
}

async function submitEditCourse(id) {
    const payload = {
        id,
        name: document.getElementById('edit-cname').value,
        title: document.getElementById('edit-ctitle').value,
        department: document.getElementById('edit-cdept').value,
        instructor: document.getElementById('edit-cinstructor').value,
        capacity: document.getElementById('edit-ccap').value,
        start_time: document.getElementById('edit-cstart').value,
        end_time: document.getElementById('edit-cend').value
    };
    showToast('Editing course...', 'warning');
    const res = await fetch(`${API_URL}/admin/courses/edit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    const data = await res.json();
    showToast(data.message || 'Course updated', data.status || 'success');
    document.getElementById('edit-modal').remove();
    await fetchState();
    renderView();
}

function renderAdminPrograms() {
    let rows = db.admin.programs.map(p => `
        <tr><td>${p.id}</td><td>${p.name}</td><td>${p.required_credits || 120}</td><td>${(p.required_courses || []).join(', ')}</td></tr>
    `).join('');
    viewContainer.innerHTML = `
        <div class="mb-6" style="display: flex; justify-content: space-between; align-items: center;">
            <h3 class="section-title">Degree Programs</h3>
            <button class="btn btn-secondary" onclick="currentView='dashboard'; renderNav(); renderView();">Back to Dashboard</button>
        </div>
        
        <div class="glass-card mb-6">
            <h3>Add New Program</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div class="form-group"><label class="form-label">Program ID</label><input type="text" id="add-pid" class="form-control" placeholder="e.g. BSc_CS"></div>
                <div class="form-group"><label class="form-label">Program Name</label><input type="text" id="add-pname" class="form-control" placeholder="Program Name"></div>
                <div class="form-group"><label class="form-label">Required Credits</label><input type="number" id="add-pcredits" class="form-control" placeholder="e.g. 120"></div>
                <div class="form-group"><label class="form-label">Required Courses</label><input type="text" id="add-pcourses" class="form-control" placeholder="Comma-separated IDs"></div>
            </div>
            <button class="btn btn-primary" onclick="addProgramUI()" style="margin-top: 1rem; width: 100%;">Create Program</button>
        </div>

        <div class="data-table-container">
            <table class="data-table">
                <thead><tr><th>ID</th><th>Name</th><th>Credits</th><th>Required Courses</th></tr></thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}
async function addProgramUI() {
    const id = document.getElementById('add-pid').value;
    const name = document.getElementById('add-pname').value;
    const credits = document.getElementById('add-pcredits').value;
    const req_courses = document.getElementById('add-pcourses').value;
    if (!id || !name) return await uiAlert("Fill fields");
    await fetch(`${API_URL}/admin/programs`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, name, credits, required_courses: req_courses }) });
    await fetchState(); renderView();
}
