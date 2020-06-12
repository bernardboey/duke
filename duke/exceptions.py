class DukeError(Exception):
    """Base class for other exceptions"""
    pass


class AlreadyDoneError(DukeError):
    """Raised when the action has already been completed"""
    def __init__(self, task_info):
        self.task_info = task_info
    pass


class TaskNumError(DukeError):
    """Raised when the input is not a valid task number"""
    def __init__(self, message="You need to provide me with a valid task number."):
        self.message = message
    pass


class ExitCommandError(DukeError):
    """Raised when the exit command is given"""
    pass


class FileCorruptError(DukeError):
    """Raised when the input file is not of the right format"""
    pass


class TaskNotFoundError(DukeError):
    """Raised when the requested task does not exist"""
    def __init__(self, task_num):
        self.task_num = task_num
        self.message = f"Task {self.task_num} does not exist."
    pass


class DateFormatError(DukeError):
    """Raised when the input date is not in the correct format"""
    def __init__(self, date_format):
        self.date_format = date_format
    pass
