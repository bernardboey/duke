import abc

from duke import exceptions
from duke import parser
from duke import ui
from duke import tasks


class Command(abc.ABC):
    def __init__(self, command_text, command_args):
        self.command_text = command_text
        self.command_args = command_args
        self.task_list = None
        self.storage = None

    def execute(self, task_list, storage):
        self.task_list = task_list
        self.storage = storage
        self._execute()

    @abc.abstractmethod
    def _execute(self):
        pass


class ExitCommand(Command):
    def _execute(self):
        raise exceptions.ExitCommandError


class AddTaskCommand(Command):
    def _execute(self):
        self.task_type = tasks.TaskType(self.command_text)
        self.add_task()
        self.storage.save_tasks(self.task_list)

    def add_task(self):
        if len(self.command_args) == 0:
            ui.output_error("You need to provide me with a task name.")
            return
        if self.task_type == tasks.TaskType.TODO:
            task_name = " ".join(self.command_args)
            self.add_task_to_task_list(task_name)
        elif self.task_type == tasks.TaskType.DEADLINE:
            self.add_task_with_date("/by")
        elif self.task_type == tasks.TaskType.EVENT:
            self.add_task_with_date("/at")
        else:
            raise RuntimeError(f"Unrecognised Task Type. {self.task_type}")

    def add_task_with_date(self, flag):
        task_type_string = self.task_type.value
        try:
            flag_index = self.command_args.index(flag)
        except ValueError:
            ui.output_error(f"You need to provide me with a {task_type_string}. Use this format:\n"
                            f"\t{task_type_string} [task name] {flag} [{task_type_string}]")
            return
        if flag_index == 0:
            ui.output_error(f"You need to provide me with a task name. Use this format:\n"
                            f"\t{task_type_string} [task name] {flag} [{task_type_string}]")
            return
        if flag_index == len(self.command_args) - 1:
            ui.output_error(f"You need to provide me with a {task_type_string}. Use this format:\n"
                            f"\t{task_type_string} [task name] {flag} [{task_type_string}]")
            return
        task_name = " ".join(self.command_args[:flag_index])
        date_string = " ".join(self.command_args[flag_index + 1:])
        self.add_task_to_task_list(task_name, date_string)

    def add_task_to_task_list(self, task_name, *args):
        try:
            _, task_info = self.task_list.add_task(self.task_type, task_name, *args)
        except exceptions.DateFormatError as e:
            ui.output_error(f"The date provided is not valid. It should be {e.date_format}.")
            return
        num_tasks = self.task_list.get_num_of_tasks()
        if num_tasks == 1:
            num_tasks = "1 task"
        else:
            num_tasks = f"{num_tasks} tasks"
        ui.output_text("Got it. I've added this task:",
                       f"  {task_info}",
                       f"Now you have {num_tasks} in the list.")


class ListCommand(Command):
    def _execute(self):
        if self.task_list.get_num_of_tasks() == 0:
            ui.output_text("Your task list is empty!")
            return
        task_list_info = self.task_list.get_info()
        task_list_string = "\n".join(task_list_info)
        ui.output_text("Here are the tasks in your list:", task_list_string)


def get_task_num(task_list, command_args):
    task_num = parser.extract_task_num(command_args)
    if task_num not in task_list:
        raise exceptions.TaskNotFoundError(task_num)
    return task_num


class DoneCommand(Command):
    def _execute(self):
        try:
            task_num = get_task_num(self.task_list, self.command_args)
        except (exceptions.TaskNotFoundError, exceptions.TaskNumError) as e:
            ui.output_error(e.message)
            return
        try:
            task_info = self.task_list.complete_task(task_num)
            self.storage.save_tasks(self.task_list)
        except exceptions.AlreadyDoneError as e:
            ui.output_text(f"Task {task_num} has already been completed.\n"
                           f"  {e.task_info}")
        else:
            ui.output_text("Nice! I've marked this task as done:\n"
                           "  " + task_info)


class DeleteCommand(Command):
    def _execute(self):
        try:
            task_num = get_task_num(self.task_list, self.command_args)
        except (exceptions.TaskNotFoundError, exceptions.TaskNumError) as e:
            ui.output_error(e.message)
            return
        task_info = self.task_list.delete_task(task_num)
        self.storage.save_tasks(self.task_list)
        num_tasks = self.task_list.get_num_of_tasks()
        if num_tasks == 1:
            num_tasks = "1 task"
        else:
            num_tasks = f"{num_tasks} tasks"
        ui.output_text(f"Noted. I've removed this task:\n"
                       f"  {task_info}",
                       f"Now you have {num_tasks} in the list.")


class HelpCommand(Command):
    def __init__(self, command_text=None, command_args=None, error_message=None):
        super().__init__(command_text, command_args)
        self.error_message = error_message

    def _execute(self):
        if self.error_message is None:
            ui.output_help_text()
        else:
            ui.output_error(self.error_message, display_help_text=True)
