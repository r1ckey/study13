import os
import json

base_dir = r"c:\Users\jorda\Documents\ANTIGRAVITY\STUDY13"
js_path = os.path.join(base_dir, "dashboard_data.js")
html_path = os.path.join(base_dir, "index.html")

# Read the current dashbaord_data.js to extract the routing mapping
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# We need to map module ID to markdown content
contents_dict = {}

id_to_path_mapping = {
    "13.1.1": "01_Internet_Basics.md",
    "13.1.2": "02_Realtime_Transmits.md",
    "13.2.1": "03_API_Paradigms.md",
    "13.2.2": "04_Data_Handling.md",
    "13.3.1": "05_Identity_Management.md",
    "13.3.2": "06_Web_Security.md",
    "13.4.1": "07_System_Architecture.md",
    "13.5.1": "08_Database_Core.md",
    "13.5.2": "09_Distributed_Data.md",
    "13.6.1": "10_Infra_LoadBalancing.md",
    "13.6.2": "11_Caching_Strategies.md",
    "13.7.1": "12_Async_Processing.md",
    "13.7.2": "13_Fault_Tolerance.md",
    "13.8.1": "14_Observability.md",
    "13.8.2": "15_DevOps_Containers.md",
    "13.9.1": "16_Data_Pipelines.md",
}

for mod_id, filename in id_to_path_mapping.items():
    md_path = os.path.join(base_dir, filename)
    if os.path.exists(md_path):
        with open(md_path, "r", encoding="utf-8") as fm:
            contents_dict[mod_id] = fm.read()

# Append the dict to dashboard_data.js if not already there
if "window.moduleContents =" not in js_content:
    new_js_content = js_content + "\n\nwindow.moduleContents = " + json.dumps(contents_dict, ensure_ascii=False, indent=2) + ";\n"
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(new_js_content)

# Update index.html to read from window.moduleContents first
with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

old_fetch_block = """            try {
                const response = await fetch(mod.path);
                if (!response.ok) throw new Error('File not found');
                const text = await response.text();
                
                mdContent.innerHTML = marked.parse(text);"""

new_fetch_block = """            try {
                let text = "";
                if (window.moduleContents && window.moduleContents[id]) {
                    text = window.moduleContents[id];
                } else {
                    const response = await fetch(mod.path);
                    if (!response.ok) throw new Error('File not found');
                    text = await response.text();
                }
                
                mdContent.innerHTML = marked.parse(text);"""

if "window.moduleContents" not in html_content:
    if old_fetch_block in html_content:
        html_content = html_content.replace(old_fetch_block, new_fetch_block)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print("Updated HTML and JS successfully.")
    else:
        print("Could not find the target fetch block in HTML.")
else:
    print("HTML already updated.")
