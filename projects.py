# ninjaapp/projects.py

projects = []

def add_project(project_data):
    projects.append(project_data)

def get_projects():
    return projects

def get_project_by_id(project_id):
    return next((p for p in projects if p["id"] == project_id), None)
