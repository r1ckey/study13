import os
import json

base_dir = r"c:\Users\jorda\Documents\ANTIGRAVITY\STUDY13"
js_path = os.path.join(base_dir, "dashboard_data.js")

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

js_content = """
const studyData = {
    title: "STUDY13",
    subtitle: "Backend Engineering",
    localStorageKey: "study13_backend_progress",
    themeColor: "#06B6D4",
    secondaryColor: "#8B5CF6",
    axes: [
        {
            title: "1. Internet & Protocols",
            modules: [
                { id: "13.1.1", title: "Web Basics (HTTP/DNS)", path: "01_Internet_Basics.md" },
                { id: "13.1.2", title: "Real-time Tx (WebSockets)", path: "02_Realtime_Transmits.md" }
            ]
        },
        {
            title: "2. API Architecture",
            modules: [
                { id: "13.2.1", title: "API Paradigms (REST/GraphQL)", path: "03_API_Paradigms.md" },
                { id: "13.2.2", title: "Data Handling (CRUD/SerDe)", path: "04_Data_Handling.md" }
            ]
        },
        {
            title: "3. Auth & Security",
            modules: [
                { id: "13.3.1", title: "IdM (AuthN/AuthZ/JWT)", path: "05_Identity_Management.md" },
                { id: "13.3.2", title: "Web Security & OWASP", path: "06_Web_Security.md" }
            ]
        },
        {
            title: "4. Architecture Patterns",
            modules: [
                { id: "13.4.1", title: "Sys Arch (Microservices/Clean)", path: "07_System_Architecture.md" }
            ]
        },
        {
            title: "5. Databases",
            modules: [
                { id: "13.5.1", title: "RDBMS vs NoSQL & Optimization", path: "08_Database_Core.md" },
                { id: "13.5.2", title: "Distributed Data (CAP/Sharding)", path: "09_Distributed_Data.md" }
            ]
        },
        {
            title: "6. Infra & Caching",
            modules: [
                { id: "13.6.1", title: "Proxies & Load Balancing", path: "10_Infra_LoadBalancing.md" },
                { id: "13.6.2", title: "Caching Strategies (Redis)", path: "11_Caching_Strategies.md" }
            ]
        },
        {
            title: "7. Async & Fault Tolerance",
            modules: [
                { id: "13.7.1", title: "Message Queues & Background", path: "12_Async_Processing.md" },
                { id: "13.7.2", title: "Resiliency (Circuit Breaker)", path: "13_Fault_Tolerance.md" }
            ]
        },
        {
            title: "8. Observability & DevOps",
            modules: [
                { id: "13.8.1", title: "Monitoring & Logging", path: "14_Observability.md" },
                { id: "13.8.2", title: "Containerization & CI/CD", path: "15_DevOps_Containers.md" }
            ]
        },
        {
            title: "9. Data Eng & Scale",
            modules: [
                { id: "13.9.1", title: "Data Pipelines (ETL/Stream)", path: "16_Data_Pipelines.md" }
            ]
        }
    ]
};
"""

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content + "\n\nwindow.moduleContents = " + json.dumps(contents_dict, ensure_ascii=False, indent=2) + ";\n")

print("Done updating dashboard data!")
