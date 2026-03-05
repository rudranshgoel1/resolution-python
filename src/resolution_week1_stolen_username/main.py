import argparse
from html import parser
import sys
import os
import json

TASKS_FILE = "tasks.json"
tasks = []

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)
    
def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str, nargs="?", help="Task to add")
    parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
    parser.add_argument("-v", "--version", help="Get the version of the app", action="version", version="1.0.0")
    parser.add_argument("-c", "--complete", type=int, help="Complete a task by entering it's ID")
    parser.add_argument("-d", "--delete", type=int, help="Delete a task by entering it's ID")
    parser.add_argument("-e", "--edit", type=int, help="Edit your task by entering it's ID")
    parser.add_argument("-r", "--reverse", type=int, help="Reverse any task to undo the completion of it by entering it's ID")
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.list:
        tasks = load_tasks()

        if len(tasks) == 0:
            print("No tasks found")
        else:
            for task in tasks:
                status = "✓" if task["done"] else " "
                print(f"[{status}] {task['id']}: {task['task']}")
            sys.exit(0)

    elif args.complete:
        tasks = load_tasks()
        for task in tasks:
            if task["id"] == args.complete:
                task["done"] = True
                name = task["task"]
                save_tasks(tasks)
                print(f"Task {name} with ID {args.complete} has been marked complete")

    elif args.reverse:
        tasks = load_tasks()
        found = False
        newlist = []
        for task in tasks:
            if task["id"] == args.reverse:
                if task["done"] == True:
                    task["done"] = False
                    name = task["task"]
                    save_tasks(tasks)
                    print(f"Task {name} with ID {args.reverse} has been marked incomplete")
                    found = True
                elif task["done"] == False:
                    name = task["task"]
                    print(f"Task {name} with ID {args.reverse} is already marked incomplete")
                    found = True

        if found:
            print("")   
        else:
            print(f"No Task with ID {args.reverse} found")

    elif args.delete:
        tasks = load_tasks()
        new_tasks = []
        for task in tasks:
            if task["id"] != args.delete:
                new_tasks.append(task)
        tasks = new_tasks
        save_tasks(new_tasks)
        print(f"Task with ID of {args.delete} deleted")

    elif args.edit:
        tasks = load_tasks()
        newlist = []
        found = False

        for task in tasks:
            if task["id"] == args.edit:
                newtask = input("Enter New task name: ")
                taskid = task["id"]
                newlist.append({"id": taskid, "task": newtask, "done": False})
                found = True
            else:
                newlist.append(task)
                
        if found:
            save_tasks(newlist)
            print(f"Task with ID {args.edit} has been edited")
        else:
            print(f"No Task with ID {args.edit} found")

    elif args.task:
        tasks = load_tasks()
        if len(tasks) == 0:
            newid = 1
        else:
            newid = tasks[-1]["id"] + 1
        tasks.append({"id": newid, "task": args.task, "done": False})
        save_tasks(tasks)

        print(f"Task {args.task} added with ID {newid}")

if __name__ == "__main__":
    main()