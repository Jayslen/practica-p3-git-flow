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

    def do_list(self, line):
        tasks_to_show = []
        task_txt = ""
        if line.strip() not in tasks_status or len(line.strip()) == 0:
            print("Showing all the tasks")
            tasks_to_show = self.tasks
        else:
            tasks_to_show = [x for x in self.tasks if x["status"] == line]
            task_txt = line

        if len(self.tasks) == 0:
            print("No tasks to show")
            return None

        rows = [list(x.values()) for x in tasks_to_show]
        columns = list(self.tasks[0].keys())

        table = Table(title=f"Tasks {task_txt}", show_lines=True, box=box.DOUBLE_EDGE)
        console = Console()

        for x in columns:
            table.add_column(x)

        for x in rows:
            row = list(x)
            row[0] = str(row[0])
            row[1] = row[1].capitalize()
            row[2] = row[2].capitalize()
            table.add_row(*row, style="magenta")

        console.print(table)

if __name__ == "__main__":
    MyCLI().cmdloop()
