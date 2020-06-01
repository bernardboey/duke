import enum
import os
from datetime import datetime

SEP = " | "
DIR_NAME = os.getcwd()
FILE_NAME = os.path.join(DIR_NAME, "data", "duke.txt")
INDENTED_HORIZONTAL_LINE = "\t" + ("_" * 50)
HELP_TEXT = ("Commands:\n"
             "\ttodo\n"
             "\tdeadline\n"
             "\tevent\n"
             "\tlist\n"
             "\tdone\n"
             "\tdelete\n"
             "\tbye")


class AlreadyDone(Exception):
    """Raised when the action has already been completed"""
    pass


@enum.unique
class TaskType(enum.Enum):
    TODO = "todo"
    DEADLINE = "deadline"
    EVENT = "event"


def prepend_tab(text):
    text_lines = text.split("\n")
    tabbed_lines = ["\t" + line for line in text_lines]
    tabbed_text = "\n".join(tabbed_lines)
    return tabbed_text


def output_text(*text_args, print_help_text=False):
    print(INDENTED_HORIZONTAL_LINE)
    for text in text_args:
        print(prepend_tab(text))
    if print_help_text:
        if len(text_args) > 0:
            print()
        print(prepend_tab(HELP_TEXT))
    print(INDENTED_HORIZONTAL_LINE)


def output_help_text():
    output_text(print_help_text=True)


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

    def get_desc(self):
        return self.task_name

    def get_completed_status(self):
        return self.is_done

    @staticmethod
    def get_additional_info():
        return None


class Todo(Task):
    TYPE_REPR = "T"
    TYPE = TaskType.TODO


class Deadline(Task):
    TYPE_REPR = "D"
    TYPE = TaskType.DEADLINE

    def __init__(self, task_name, deadline):
        Task.__init__(self, task_name)
        self._deadline = deadline

    @property
    def deadline(self):
        return datetime.strftime(self._deadline, "%d %b %Y")

    def get_desc(self):
        return f"{self.task_name} (by: {self.deadline})"

    def get_additional_info(self):
        return self.deadline


class Event(Task):
    TYPE_REPR = "E"
    TYPE = TaskType.EVENT

    def __init__(self, task_name, date_time):
        Task.__init__(self, task_name)
        self._date_time = date_time

    @property
    def date_time(self):
        return datetime.strftime(self._date_time, "%d %b %Y")

    def get_desc(self):
        return f"{self.task_name} (at: {self.date_time})"

    def get_additional_info(self):
        return self.date_time


class TaskList:
    def __init__(self):
        self.tasks = []
        self.DICT_OF_TASK_TYPES_TO_CLASS = {TaskType.TODO: Todo,
                                            TaskType.DEADLINE: Deadline,
                                            TaskType.EVENT: Event}

    def get_num_of_tasks(self):
        return len(self.tasks)

    def get_task(self, task_num):
        if task_num <= 0 or task_num > self.get_num_of_tasks():
            return None
        task_id = task_num - 1
        task = self.tasks[task_id]
        return task

    def add_task(self, task_type, task_name, *args):
        task_class = self.DICT_OF_TASK_TYPES_TO_CLASS[task_type]
        new_task = task_class(task_name, *args)
        self.tasks.append(new_task)
        return new_task

    @staticmethod
    def complete_task(task):
        task.complete()

    def delete_task(self, task):
        self.tasks.remove(task)

    def delete_all_tasks(self):
        self.tasks.clear()

    @staticmethod
    def get_task_info(task):
        desc = task.get_desc()
        type_repr = task.TYPE_REPR
        is_done = task.get_completed_status()
        if is_done:
            done_symbol = "✓"
        else:
            done_symbol = "✗"
        return f"[{type_repr}][{done_symbol}] {desc}"

    def get_numbered_task_info(self, task):
        task_info = self.get_task_info(task)
        task_id = self.tasks.index(task)
        task_num = task_id + 1
        return f"{task_num}.{task_info}"

    def get_info(self):
        return [self.get_numbered_task_info(task) for task in self.tasks]

    def save_tasks(self):
        with open(FILE_NAME, "w") as file:
            for task in self.tasks:
                type_repr = task.TYPE.value
                is_done = str(int(task.get_completed_status()))
                task_name = task.task_name
                file.write(type_repr + SEP + is_done + SEP + task_name)
                additional_info = task.get_additional_info()
                if additional_info is None:
                    file.write("\n")
                else:
                    file.write(SEP + additional_info + "\n")

    def parse_tasks(self, lines):
        try:
            for line in lines:
                line = line.rstrip('\n')
                attributes = line.split(SEP)
                task_type_string = attributes[0]
                task_type = TaskType(task_type_string)
                task_is_done = attributes[1]
                task_name = attributes[2]
                if len(attributes) > 3:
                    task_additional_info = attributes[3]
                    new_task = self.add_task(task_type, task_name, task_additional_info)
                else:
                    new_task = self.add_task(task_type, task_name)
                if task_is_done == "1":
                    new_task.complete()
                elif task_is_done != "0":
                    raise ValueError("Saved filed is not in the proper format")
            print("Successfully loaded file.")
        except (LookupError, ValueError):
            self.delete_all_tasks()
            print("Saved filed is not in the proper format. Creating task list from scratch.")


def add_task_to_task_list(task_list, task_type, task_name, *args):
    _ = task_list.add_task(task_type, task_name, *args)
    num_tasks = task_list.get_num_of_tasks()
    task = task_list.get_task(num_tasks)
    task_info = task_list.get_task_info(task)
    if num_tasks == 1:
        num_tasks = "1 task"
    else:
        num_tasks = f"{num_tasks} tasks"
    output_text("Got it. I've added this task:",
                f"  {task_info}",
                f"Now you have {num_tasks} in the list.")


def get_date(date_string):
    for date_format in ("%d/%m/%Y", "%d/%m/%y", "%d %b %Y", "%d %b", "%d-%m-%Y", "%d-%m-%y"):
        try:
            date = datetime.strptime(date_string, date_format)
            return date
        except ValueError:
            continue
    raise ValueError("Date string does not conform to any of the date formats.")


def add_task_with_date(task_list, task_type, command_args, flag):
    task_type_string = task_type.value
    try:
        flag_index = command_args.index(flag)
    except ValueError:
        output_text(f"☹ OOPS!!! You need to provide me with a {task_type_string}. Use this format:\n"
                    f"{task_type_string} [task name] {flag} [{task_type_string}]")
        return
    if flag_index == 0:
        output_text("☹ OOPS!!! You need to provide me with a task name. Use this format:\n"
                    f"{task_type_string} [task name] {flag} [{task_type_string}]")
        return
    if flag_index == len(command_args) - 1:
        output_text(f"☹ OOPS!!! You need to provide me with a {task_type_string}. Use this format:\n"
                    f"{task_type_string} [task name] {flag} [{task_type_string}]")
        return
    task_name = " ".join(command_args[:flag_index])
    date_string = " ".join(command_args[flag_index + 1:])
    try:
        date = get_date(date_string)
    except ValueError:
        output_text(f"☹ OOPS!!! The date provided is not valid. It should be dd/mm/yy")
        return
    add_task_to_task_list(task_list, task_type, task_name, date)


def add_task(task_list, task_type, command_args):
    if len(command_args) == 0:
        output_text("☹ OOPS!!! You need to provide me with a task name.")
        return
    if task_type == TaskType.TODO:
        task_name = " ".join(command_args)
        add_task_to_task_list(task_list, task_type, task_name)
    elif task_type == TaskType.DEADLINE:
        add_task_with_date(task_list, task_type, command_args, "/by")
    elif task_type == TaskType.EVENT:
        add_task_with_date(task_list, task_type, command_args, "/at")


def print_tasks(task_list):
    if task_list.get_num_of_tasks() == 0:
        output_text("Your task list is empty!")
        return
    task_list_info = task_list.get_info()
    task_list_string = "\n".join(task_list_info)
    output_text("Here are the tasks in your list:", task_list_string)


def extract_task_num_from_args(command_args):
    if len(command_args) == 0:
        output_text("☹ OOPS!!! You need to provide me with a task number.")
        return None
    if len(command_args) > 1:
        output_text("☹ OOPS!!! There are too many spaces. Please provide me with a valid task number.")
        return None
    try:
        task_num = int(command_args[0])
    except ValueError:
        output_text("☹ OOPS!!! That's not a number!")
        raise ValueError("Expected a number")
    if task_num <= 0:
        output_text("☹ OOPS!!! You need to provide me with a valid task number.")
        raise ValueError("Expected a valid task number")
    return task_num


def get_task(task_list, task_num):
    task = task_list.get_task(task_num)
    if task is None:
        output_text(f"☹ OOPS!!! Task {task_num} does not exist.")
        raise ValueError("Task does not exist")
    return task


def complete_task(task_list, command_args):
    try:
        task_num = extract_task_num_from_args(command_args)
        task = get_task(task_list, task_num)
    except ValueError:
        return
    try:
        task_list.complete_task(task)
    except AlreadyDone:
        task_info = task_list.get_task_info(task)
        output_text(f"Task {task_num} has already been completed.\n"
                    "  " + task_info)
        return
    task_info = task_list.get_task_info(task)
    output_text("Nice! I've marked this task as done:\n"
                "  " + task_info)


def delete_task(task_list, command_args):
    try:
        task_num = extract_task_num_from_args(command_args)
        task = get_task(task_list, task_num)
    except ValueError:
        return
    task_info = task_list.get_task_info(task)
    task_list.delete_task(task)
    num_tasks = task_list.get_num_of_tasks()
    if num_tasks == 1:
        num_tasks = "1 task"
    else:
        num_tasks = f"{num_tasks} tasks"
    output_text("Noted. I've removed this task:\n"
                "  " + task_info,
                f"Now you have {num_tasks} in the list.")


def main():
    task_list = TaskList()
    try:
        with open(FILE_NAME) as file:
            print("Loading task list from file...")
            if os.stat(FILE_NAME).st_size == 0:
                raise ValueError()
            lines = file.readlines()
            task_list.parse_tasks(lines)
    except FileNotFoundError:
        print("No file detected. Creating task list from scratch.")
    except ValueError:
        print("File empty. Creating task list from scratch.")
    greet()
    while True:
        full_command = input()
        input_list = full_command.split()
        try:
            command = input_list[0]
            command_args = input_list[1:]
        except IndexError:
            command = "error"
            command_args = None
        if full_command == "bye":
            say_goodbye()
            return
        elif command in ("todo", "deadline", "event"):
            add_task(task_list, TaskType(command), command_args)
            task_list.save_tasks()
        elif full_command == "list":
            print_tasks(task_list)
        elif command == "done":
            complete_task(task_list, command_args)
            task_list.save_tasks()
        elif command == "delete":
            delete_task(task_list, command_args)
            task_list.save_tasks()
            pass
        else:
            output_text("☹ OOPS!!! I'm sorry, but I don't know what that means :-(", print_help_text=True)


if __name__ == "__main__":
    main()
