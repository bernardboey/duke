import os

import duke.task_list
from duke import exceptions
from duke import tasks
from duke import ui
from duke import utils

SEP = " | "


class Storage:
    def __init__(self, file_path):
        self._file_path = file_path

    def save_tasks(self, task_list):
        with open(self._file_path, "w") as file:
            for task in task_list.tasks:
                type_repr = task.type.value
                is_done = str(int(task.is_done))
                task_name = task.task_name
                file.write(type_repr + SEP + is_done + SEP + task_name)
                additional_info = task.get_additional_info()
                if additional_info is None:
                    file.write("\n")
                else:
                    file.write(SEP + additional_info + "\n")

    def load_tasks(self):
        task_list = duke.task_list.TaskList()
        ui.show_loading_text()
        try:
            with open(self._file_path) as file:
                if os.stat(self._file_path).st_size == 0:
                    raise EOFError()
                lines = file.readlines()
                Storage.parse_tasks(task_list, lines)
        except FileNotFoundError:
            ui.show_failed_load_text(f"File ({self._file_path}) not found.")
        except EOFError:
            ui.show_failed_load_text(f"File ({self._file_path}) is empty.")
        except (LookupError, ValueError, exceptions.FileCorruptError):
            ui.show_failed_load_text(f"Saved file ({self._file_path}) is not in the proper format.")
            task_list = duke.task_list.TaskList()
        except Exception as e:
            raise e
        else:
            ui.show_successful_load_text()
        finally:
            return task_list

    @staticmethod
    def parse_tasks(task_list, lines):
        for line in lines:
            line = line.rstrip('\n')
            attributes = line.split(SEP)
            task_type_string = attributes[0]
            task_type = tasks.TaskType(task_type_string)
            task_is_done = attributes[1]
            task_name = attributes[2]
            if len(attributes) > 3:
                task_additional_info = attributes[3]
                new_task, _ = task_list.add_task(task_type, task_name, task_additional_info)
            else:
                new_task, _ = task_list.add_task(task_type, task_name)
            if task_is_done == "1":
                new_task.complete()
            elif task_is_done != "0":
                raise exceptions.FileCorruptError
