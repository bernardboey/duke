import enum

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


class Todo(Task):
    TYPE_REPR = "T"


class Deadline(Task):
    TYPE_REPR = "D"

    def __init__(self, task_name, deadline):
        Task.__init__(self, task_name)
        self.deadline = deadline

    def get_desc(self):
        return f"{self.task_name} (by: {self.deadline})"


class Event(Task):
    TYPE_REPR = "E"

    def __init__(self, task_name, date_time):
        Task.__init__(self, task_name)
        self.date_time = date_time

    def get_desc(self):
        return f"{self.task_name} (at: {self.date_time})"


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

    @staticmethod
    def complete_task(task):
        task.complete()

    def delete_task(self, task):
        self.tasks.remove(task)

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


def add_task_to_task_list(task_list, task_type, task_name, *args):
    task_list.add_task(task_type, task_name, *args)
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


def add_task_with_additional_parameter(task_list, task_type, command_args, flag):
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
    additional_parameter = " ".join(command_args[flag_index + 1:])
    add_task_to_task_list(task_list, task_type, task_name, additional_parameter)


def add_task(task_list, task_type, command_args):
    if len(command_args) == 0:
        output_text("☹ OOPS!!! You need to provide me with a task name.")
        return
    if task_type == TaskType.TODO:
        task_name = " ".join(command_args)
        add_task_to_task_list(task_list, task_type, task_name)
    elif task_type == TaskType.DEADLINE:
        add_task_with_additional_parameter(task_list, task_type, command_args, "/by")
    elif task_type == TaskType.EVENT:
        add_task_with_additional_parameter(task_list, task_type, command_args, "/at")


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


def handle_user_input():
    task_list = TaskList()
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
        elif command in ["todo", "deadline", "event"]:
            add_task(task_list, TaskType(command), command_args)
        elif full_command == "list":
            print_tasks(task_list)
        elif command == "done":
            complete_task(task_list, command_args)
        elif command == "delete":
            delete_task(task_list, command_args)
            pass
        else:
            output_text("☹ OOPS!!! I'm sorry, but I don't know what that means :-(", print_help_text=True)


def main():
    greet()
    handle_user_input()


if __name__ == "__main__":
    main()
