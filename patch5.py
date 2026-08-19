import re

with open("frontend/app.js", "r") as f:
    js = f.read()

modal_code = """
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
"""

if "// --- CUSTOM UI MODALS ---" not in js:
    js = modal_code + "\n" + js

js = js.replace('prompt("Enter new capacity for this course:");', 'await uiPrompt("Enter new capacity for this course:");')
js = js.replace('alert(msg);', 'await uiAlert(msg);')
js = js.replace('alert("Description Update Request Sent!");', 'await uiAlert("Description Update Request Sent!");')
js = js.replace('alert("Prerequisite Update Request Sent!");', 'await uiAlert("Prerequisite Update Request Sent!");')
js = js.replace('prompt("Enter new description:");', 'await uiPrompt("Enter new description:");')
js = js.replace('prompt("Enter prerequisite course ID:");', 'await uiPrompt("Enter prerequisite course ID:");')
js = js.replace('alert("Fill fields");', 'await uiAlert("Fill fields");')
js = js.replace('prompt("Enter new name for " + id + ":", oldName);', 'await uiPrompt("Enter new name for " + id + ":", oldName);')
js = js.replace('confirm("Deactivate " + id + "?")', 'await uiConfirm("Deactivate " + id + "?")')
js = js.replace('prompt("Enter new capacity:");', 'await uiPrompt("Enter new capacity:");')
js = js.replace('alert(data.stats);', 'await uiAlert(data.stats);')
js = js.replace('alert(data.workload);', 'await uiAlert(data.workload);')
js = js.replace('alert(data.popularity);', 'await uiAlert(data.popularity);')

with open("frontend/app.js", "w") as f:
    f.write(js)
print("UI Custom Modals Applied!")
