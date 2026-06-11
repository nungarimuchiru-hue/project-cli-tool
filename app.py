import argparse
import json
import os


DATA_FILE = "data.json"


class Task:
    def __init__(self, title):
        self.title = title
        self.completed = False


class Project:
    def __init__(self, title):
        self.title = title
        self.tasks = []


class User:
    def __init__(self, name):
        self.name = name
        self.projects = []

        
# Load data from file
def load_data():
    # If file does not exist, return empty structure
    if not os.path.exists(DATA_FILE):
        return {"users": []}

    # Open file and read JSON data
    with open(DATA_FILE, "r") as file:
        return json.load(file)


# Save data to JSON file
def save_data(data):
    # Write updated data back to file
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Add a new user
def add_user(name):
    data = load_data()

    # Check if user already exists
    for user in data["users"]:
        if user["name"] == name:
            print("User already exists!")
            return

    # Add new user with empty project list
    data["users"].append({
        "name": name,
        "projects": []
    })

    save_data(data) # type: ignore
    print(f"User '{name}' added successfully!")
# Add project to a user
def add_project(user_name, project_title):
    data = load_data()

    # Find the user
    for user in data["users"]:
        if user["name"] == user_name:
            # Add project under user
            user["projects"].append({
                "title": project_title,
                "tasks": []
            })

            save_data(data) # type: ignore
            print(f"project '{project_title}' added to {user_name}")
            return
        
        print("User not found!")


# Add task to a project
def add_task(project_title, task_title):
    data = load_data()

    # Find project inside any user
    for user in data["users"]:
        for project in user["projects"]:
            if project["title"] == project_title:

                # Add task to project
                project["tasks"].append({
                   "title": task_title,
                   "completed": False 
                })

                save_data(data) # type: ignore
                print(f"Task '{task_title}' added to project '{project_title}'")
                return
            
            print("project not found!")

          
# List all users
def list_users():
    data = load_data()

    print("\nUsers:")
    for user in data["users"]:
        print("-", user["name"])


# List projects for a specific user
def list_projects(user_name):
    data = load_data()

    # Find user and display projects
    for user in data["users"]:
        if user["name"] == user_name:
            print(f"\nProjects for {user_name}:")
            for project in user["projects"]:
                print("-", project["title"])
            return

    print("User not found!")


# Mark task as completed
def complete_task(task_title):
    data = load_data()

    # Search for task in all projects
    for user in data["users"]:
        for project in user["projects"]:
            for task in project["tasks"]:
                if task["title"] == task_title:

                    # Mark task as complete
                    task["completed"] = True

                    save_data(data) # type: ignore
                    print(f"Task '{task_title}' marked as complete!")
                    return

    print("Task not found!")


# CLI setup using argparse
parser = argparse.ArgumentParser(description="Project Management CLI Tool")
subparsers = parser.add_subparsers(dest="command")


# Command: add-user
parser_add_user = subparsers.add_parser("add-user")
parser_add_user.add_argument("--name", required=True)


# Command: add-project
parser_add_project = subparsers.add_parser("add-project")
parser_add_project.add_argument("--user", required=True)
parser_add_project.add_argument("--title", required=True)


# Command: add-task
parser_add_task = subparsers.add_parser("add-task")
parser_add_task.add_argument("--project", required=True)
parser_add_task.add_argument("--title", required=True)


# Command: list-users
subparsers.add_parser("list-users")


# Command: list-projects
parser_list_projects = subparsers.add_parser("list-projects")
parser_list_projects.add_argument("--user", required=True)


# Command: complete-task
parser_complete = subparsers.add_parser("complete-task")
parser_complete.add_argument("--title", required=True)


args = parser.parse_args()


# Run selected command
if args.command == "add-user":
    add_user(args.name)

elif args.command == "add-project":
    add_project(args.user, args.title)

elif args.command == "add-task":
    add_task(args.project, args.title)

elif args.command == "list-users":
    list_users()

elif args.command == "list-projects":
    list_projects(args.user)

elif args.command == "complete-task":
    complete_task(args.title)

else:
    print("Use --help to see available commands")          