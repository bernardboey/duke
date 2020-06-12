import os

from duke.storage import Storage
from duke import parser
from duke import ui
from duke import exceptions

DIR_NAME = os.getcwd()
FILE_PATH = os.path.join(DIR_NAME, "data", "duke.txt")


def main():
    storage = Storage(FILE_PATH)
    task_list = storage.load_tasks()
    ui.greet()
    while True:
        try:
            full_command_text = input()
            command = parser.parse_command(full_command_text)
            command.execute(task_list, storage)
        except exceptions.ExitCommandError:
            ui.say_goodbye()
            return


if __name__ == "__main__":
    main()
