import streamlit as st
import sqlite3
import json

def create_table():
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            data TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_project(name, data):
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO projects (name, data) VALUES (?, ?)", (name, json.dumps(data)))
    conn.commit()
    conn.close()

def list_projects():
    conn = sqlite3.connect("projects.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, data FROM projects ORDER BY id DESC")
    projects = cursor.fetchall()
    conn.close()
    return projects

create_table()

st.set_page_config(page_title="DevOps Bootstrap Generator", layout="wide")
st.title("DevOps CI/CD Generator - GitLab")

if "form_data" not in st.session_state:
    st.session_state.form_data = {}

tabs = st.tabs([
    "1 - Project Info",
    "2 - Technologies",
    "3 - Dependencies",
    "4 - Pipeline",
    "Generate Pipeline",
    "Saved Projects"
])

with tabs[0]:
    st.header("Project Information")
    project_name = st.text_input("Project Name", key="project_name")
    description = st.text_area("Description")

    if project_name:
        st.session_state.form_data["project_name"] = project_name
        st.session_state.form_data["description"] = description

with tabs[1]:
    st.header("🛠️ Technologies")

    language = st.selectbox("Programming Language", ["Java", "C#", "Node"])

    java_versions = ["17", "21", "8"]
    dotnet_versions = ["6.0", "7.0", "8.0"]
    node_versions = ["14.x", "16.x", "18.x"]

    version = st.selectbox(
        "Language Version",
        java_versions if language == "Java" else dotnet_versions
    )

    java_frameworks = {
        "Spring Boot": "3.2.x",
        "Hibernate": "6.3.x",
        "JUnit": "5.x"
    }

    dotnet_frameworks = {
        "ASP.NET Core": "8.0",
        "Entity Framework": "8.0",
        "xUnit": "2.4",
        "Serilog": "3.x"
    }
    node_frameworks = {
        "Express": "4.x",
        "NestJS": "9.x",
        "Jest": "29.x"
    }

    frameworks_dict = java_frameworks if language == "Java" else dotnet_frameworks

    selected_frameworks = st.multiselect(
        "Frameworks/Libraries",
        options=list(frameworks_dict.keys()),
        format_func=lambda f: f"{f} ({frameworks_dict[f]})"
    )

    database = st.selectbox("Database", ["PostgreSQL", "SQL Server", "MySQL"])
    ansible_roles = st.multiselect("Ansible Roles", ["nginx", "docker", "git", "java", "dotnet"])
    monitoring = st.checkbox("Use Grafana + Prometheus")

    st.session_state.form_data.update({
        "language": language,
        "version": version,
        "frameworks": selected_frameworks,
        "database": database,
        "ansible_roles": ansible_roles,
        "monitoring": monitoring,
    })

with tabs[2]:
    st.header("Project Dependencies")
    deps = st.text_area("List dependencies (one per line)", placeholder="e.g., lombok, jackson, swashbuckle...")
    dependencies = deps.splitlines() if deps else []

    st.session_state.form_data["dependencies"] = dependencies

with tabs[3]:
    st.header("Pipeline Configuration")

    steps = st.multiselect("Select pipeline steps", ["Build", "Test", "SAST", "DAST", "Deploy"])
    environment = st.selectbox("Target Environment", ["DEV", "UAT", "PROD"])

    st.session_state.form_data["steps"] = steps
    st.session_state.form_data["environment"] = environment

with tabs[4]:
    st.header("GitLab CI/CD YAML Preview")

    data = st.session_state.form_data

    if "project_name" not in data:
        st.error("Please fill out at least the Project Name in the first tab.")
    else:
        ci_yml = f"""
# Project: {data['project_name']}
# Description: {data.get('description', '')}
# Language: {data.get('language', '')} {data.get('version', '')}
# Frameworks: {', '.join(data.get('frameworks', []))}
# Database: {data.get('database', '')}
# Environment: {data.get('environment', '')}
# Monitoring: {'Yes' if data.get('monitoring') else 'No'}

stages:
{chr(10).join([f"  - {s.lower()}" for s in data.get('steps', [])])}

{chr(10).join([f"""
{s.lower()}:
    stage: {s.lower()}
    script:
    - echo '{s} running...'
""" for s in data.get('steps', [])])}
"""

        st.code(ci_yml, language="yaml")

        if st.button("Save to Database"):
            save_project(data["project_name"], data)
            st.success("Project saved successfully!")

        st.download_button("Download .gitlab-ci.yml", ci_yml, file_name=".gitlab-ci.yml")

with tabs[5]:
    st.header("Saved Projects")

    projects = list_projects()

    if not projects:
        st.info("No projects saved yet.")
    else:
        for id, name, data in projects:
            data_dict = json.loads(data)
            with st.expander(f"{name}"):
                st.markdown(f"**Description:** {data_dict.get('description', '-')}")
                st.markdown(f"**Language:** {data_dict.get('language')} {data_dict.get('version')}")
                st.markdown(f"**Frameworks:** {', '.join(data_dict.get('frameworks', []))}")
                st.markdown(f"**Database:** {data_dict.get('database', '-')}")
                st.markdown(f"**Monitoring:** {'✅' if data_dict.get('monitoring') else '❌'}")
                st.markdown(f"**Pipeline Steps:** {', '.join(data_dict.get('steps', []))}")
                st.markdown(f"**Environment:** {data_dict.get('environment', '-')}")

                if st.checkbox(f"View .gitlab-ci.yml for {name}", key=f"preview_{id}"):
                    ci_yml = f"""
# Project: {name}
# Language: {data_dict.get('language')} {data_dict.get('version')}
# Frameworks: {', '.join(data_dict.get('frameworks', []))}

stages:
{chr(10).join([f"  - {s.lower()}" for s in data_dict.get('steps', [])])}

{chr(10).join([f"""
{s.lower()}:
    stage: {s.lower()}
    script:
    - echo '{s} running...'
""" for s in data_dict.get('steps', [])])}
"""
                    st.code(ci_yml, language="yaml")
