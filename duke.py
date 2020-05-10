import pytest

INDENTED_HORIZONTAL_LINE = "\t" + ("_" * 50)


class AlreadyDone(Exception):
    """Raised when the action has already been completed"""
    pass


def output_text(*text_args):
    print(INDENTED_HORIZONTAL_LINE)
    for text in text_args:
        text_lines = text.split("\n")
        for line in text_lines:
            print("\t" + line)
    print(INDENTED_HORIZONTAL_LINE)


def greet():
    output_text("Hello! I'm Duke's friend, Python!\n"
                "What can I do for you?")


def say_goodbye():
    output_text("Bye. Hope to see you again soon!")


class Task:
    def __init__(self, task_name):
        self.task_name = task_name
        self.is_done = False

    def complete(self):
        if self.is_done:
            raise AlreadyDone("Task already completed")
        self.is_done = True

    def get_name(self):
        return self.task_name

    def get_completed_status(self):
        return self.is_done

    pass


class Tasks:
    def __init__(self):
        self.tasks = {}
        self.num_of_tasks = 0

    def add_task(self, task_name):
        next_task_num = self.num_of_tasks + 1
        self.tasks[next_task_num] = Task(task_name)
        self.num_of_tasks += 1

    def complete_task(self, task_num):
        try:
            self.tasks[task_num].complete()
            return self.tasks[task_num].get_name()
        except KeyError:
            return None

    def get_info(self):
        return [(i, task.get_name(), task.get_completed_status()) for i, task in self.tasks.items()]


def print_tasks(task_list):
    task_list_info = task_list.get_info()
    tasks = []
    for i, task_name, is_done in task_list_info:
        if is_done:
            symbol = "✓"
        else:
            symbol = "✗"
        tasks.append(f"{i}.[{symbol}] {task_name}")
    task_list_string = "\n".join(tasks)
    output_text("Here are the tasks in your list:", task_list_string)


def extract_num_from_command_suffix(command_suffix):
    try:
        if command_suffix[0] != " ":
            raise ValueError("there should be a space after 'done'")
        num = int(command_suffix[1:])
        return num
    except (IndexError, ValueError):
        return None


def try_to_complete_task(task_list, command):
    task_num = extract_num_from_command_suffix(command[4:])
    if task_num is None:
        output_text("'Done' command should be of the following format:\n"
                    "\tdone [task number]")
    else:
        try:
            task_name = task_list.complete_task(task_num)
        except AlreadyDone:
            output_text(f"Task {task_num} has already been completed.")  # maybe add the task name here
            return
        if task_name is None:
            output_text(f"Task {task_num} does not exist.")
            return
        output_text("Nice! I've marked this task as done:\n"
                    "  [✓] " + task_name)


def save_task(task_list, task):
    task_list.add_task(task)
    output_text("added: " + task)


def handle_user_input():
    task_list = Tasks()
    while True:
        command = input()
        if command == "bye":
            say_goodbye()
            return
        elif command == "list":
            print_tasks(task_list)
        elif command[:4] == "done":
            try_to_complete_task(task_list, command)
        else:
            save_task(task_list, task=command)


def main():
    greet()
    handle_user_input()


if __name__ == "__main__":
    main()
