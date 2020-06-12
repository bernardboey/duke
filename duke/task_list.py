from duke import exceptions
from duke import tasks


class TaskList:
    DICT_OF_TASK_TYPES_TO_CLASS = {tasks.TaskType.TODO: tasks.Todo,
                                   tasks.TaskType.DEADLINE: tasks.Deadline,
                                   tasks.TaskType.EVENT: tasks.Event}

    def __init__(self):
        self.tasks = []

    def get_num_of_tasks(self):
        return len(self.tasks)

    def get_task(self, task_num):
        if task_num not in self:
            raise exceptions.TaskNotFoundError(task_num)
        task_id = task_num - 1
        task = self.tasks[task_id]
        return task

    def add_task(self, task_type, task_name, *args):
        task_class = self.DICT_OF_TASK_TYPES_TO_CLASS[task_type]
        new_task = task_class(task_name, *args)
        task_info = new_task.get_task_info()
        self.tasks.append(new_task)
        return new_task, task_info

    def delete_all_tasks(self):
        self.tasks.clear()

    def get_task_num(self, task):
        task_id = self.tasks.index(task)
        task_num = task_id + 1
        return task_num

    def get_numbered_task_info(self, task):
        task_info = task.get_task_info()
        task_num = self.get_task_num(task)
        return f"{task_num}.{task_info}"

    def get_info(self):
        return [self.get_numbered_task_info(task) for task in self.tasks]

    def __contains__(self, task_num):
        return 0 < task_num <= self.get_num_of_tasks()

    def complete_task(self, task_num):
        if task_num not in self:
            raise exceptions.TaskNotFoundError(task_num)
        task = self.get_task(task_num)
        try:
            task.complete()
        except exceptions.AlreadyDoneError as e:
            raise e
        else:
            return task.get_task_info()

    def delete_task(self, task_num):
        if task_num not in self:
            raise exceptions.TaskNotFoundError(task_num)
        task = self.get_task(task_num)
        task_info = task.get_task_info()
        self.tasks.remove(task)
        return task_info
