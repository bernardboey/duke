import abc
import datetime
import enum

from duke import exceptions
from duke import utils


@enum.unique
class TaskType(enum.Enum):
    TODO = "todo"
    DEADLINE = "deadline"
    EVENT = "event"


class Task(abc.ABC):
    def __init__(self, task_name):
        self.task_name = task_name
        self.is_done = False

    def complete(self):
        if self.is_done:
            raise exceptions.AlreadyDoneError(self.get_task_info())
        self.is_done = True

    def get_desc(self):
        return self.task_name

    def get_additional_info(self):
        return None

    def get_task_info(self):
        desc = self.get_desc()
        type_repr = self.type_repr
        if self.is_done:
            done_symbol = "✓"
        else:
            done_symbol = "✗"
        return f"[{type_repr}][{done_symbol}] {desc}"

    @property
    @abc.abstractmethod
    def type_repr(self):
        pass

    @property
    @abc.abstractmethod
    def type(self):
        pass


class Todo(Task):
    type_repr = "T"
    type = TaskType.TODO


class Deadline(Task):
    type_repr = "D"
    type = TaskType.DEADLINE

    def __init__(self, task_name, date_string):
        super().__init__(task_name)
        self._deadline = utils.get_date(date_string)

    @property
    def deadline(self):
        return datetime.datetime.strftime(self._deadline, "%d %b %Y")

    def get_desc(self):
        return f"{self.task_name} (by: {self.deadline})"

    def get_additional_info(self):
        return self.deadline


class Event(Task):
    type_repr = "E"
    type = TaskType.EVENT

    def __init__(self, task_name, datetime_string):
        super().__init__(task_name)
        self._datetime = utils.get_date(datetime_string)  # TODO: Change to utils.get_datetime

    @property
    def date_time(self):
        return datetime.datetime.strftime(self._datetime, "%d %b %Y")  # TODO: Change to time format

    def get_desc(self):
        return f"{self.task_name} (at: {self.date_time})"

    def get_additional_info(self):
        return self.date_time
