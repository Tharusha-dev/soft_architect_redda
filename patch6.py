import re

with open("frontend/app.js", "r") as f:
    js = f.read()

# 1. Point the sidebar 'courses' route to our new CRUD UI
js = js.replace("else if (currentView === 'courses') renderAdminCourses();", "else if (currentView === 'courses') renderAdminCoursesCRUD();")


# 2. Fix Reports UI
old_reports = """function renderAdminReports() {
    viewContainer.innerHTML = `
        <div class="mb-6">
            <h3 class="section-title">Reporting & Analytics</h3>
        </div>
        <div class="grid-cards">
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-chart-line" style="font-size: 3rem; color: var(--primary); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Enrolment Trends</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); text-align: center; margin-bottom: 1.5rem;">Analyze enrolment data across departments and semesters.</p>
                <button class="btn btn-primary" onclick="generateReport('stats')">Generate Report</button>
            </div>
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-user-graduate" style="font-size: 3rem; color: var(--accent); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Instructure Workload</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); text-align: center; margin-bottom: 1.5rem;">Review course assignments and credit hours per instructure.</p>
                <button class="btn btn-primary" onclick="generateReport('workload')">Generate Report</button>
            </div>
            <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 3rem 2rem;">
                <i class="fa-solid fa-fire" style="font-size: 3rem; color: var(--warning); margin-bottom: 1rem;"></i>
                <h4 style="margin-bottom: 0.5rem;">Course Popularity</h4>
                <p style="font-size: 0.875rem; color: var(--text-muted); text-align: center; margin-bottom: 1.5rem;">Identify high-demand courses for resource allocation.</p>
                <button class="btn btn-primary" onclick="generateReport('popularity')">Generate Report</button>
            </div>
        </div>
    `;
}

async function generateReport(type) {
    showToast('Generating report via Template Method...', 'warning');
    const res = await fetch('http://localhost:5000/api/admin/reports');
    const data = await res.json();
    
    if (type === 'stats') await uiAlert(data.stats);
    if (type === 'workload') await uiAlert(data.workload);
    if (type === 'popularity') await uiAlert(data.popularity);
}"""

new_reports = """function renderAdminReports() {
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
}"""

js = js.replace(old_reports, new_reports)

with open("frontend/app.js", "w") as f:
    f.write(js)
print("Sixth patch applied: Fixed Sidebar route and enhanced Reports UI.")
