import cmd
import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich import box

task_done = "done"
task_in_progress = "in progress"
task_todo = "todo"
tasks_status = [task_done, task_in_progress, task_todo]


class MyCLI(cmd.Cmd):
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.id = 0

    prompt = "task-cli > "
    intro = "Welcome to track list CLI app, write help, to get all the commands"

    # FOR TESTING
    def test_start(self):
        self.preloop()

    def preloop(self):
        if not os.path.exists("tasks.json"):
            with open("tasks.json", "w") as file:
                file.write("[]")
        else:
            with open("tasks.json", "r+") as f:
                try:
                    self.update_tasks(json.load(f))
                except json.JSONDecodeError:
                    f.write("[]")

    def postloop(self):
        self.update_file()

    def do_help(self, line):
        console = Console()
        console.print(
            "You can perform certaint actions with these commands \n help: Get all the commands \n add: Add a task \n list: show all task saved \n list done: show all done tasks \n list in progress: show all task in progress \n list todo: show task to do \n mark_done {id}: mark the task selected as done \n mark_in_progress {id}:mark the task selected as in progress \n delete {id} delete a task providing the id of it \n update {id} new name: Edit a taks"
        )

    def create_task(self, name):
        return {
            "id": self.id,
            "task": name.lower(),
            "status": task_todo.lower(),
            "created_at": f"{datetime.now()}",
            "updated_at": f"{datetime.now()}",
        }



    def do_add(self, line):
        if len(line.strip()) < 4:
            print("Task name too short try other")
            return None

        new_task = self.create_task(line)
        self.tasks.append(new_task)
        self.id = self.tasks[len(self.tasks) - 1]["id"] + 1
        self.update_file()
        print(f"Task {line.upper()} added")

if __name__ == "__main__":
    MyCLI().cmdloop()
