from duke import commands
from duke import exceptions
from duke import tasks

COMMANDS_WITH_NO_ARGS = {
    "list": commands.ListCommand,
    "bye": commands.ExitCommand,
    "help": commands.HelpCommand
}

ADD_TASK_COMMANDS = {
    TASK_TYPE.value: commands.AddTaskCommand for TASK_TYPE in tasks.TaskType
}

COMMANDS_WITH_ARGS = {
    **ADD_TASK_COMMANDS,
    "done": commands.DoneCommand,
    "delete": commands.DeleteCommand
}


def parse_command(full_command_text):
    input_list = full_command_text.split()
    if not input_list:
        return commands.HelpCommand(error_message="Please type a command.")
    command_text = input_list[0]
    command_args = input_list[1:]
    if command_text in COMMANDS_WITH_NO_ARGS:
        return COMMANDS_WITH_NO_ARGS[full_command_text](command_text, command_args)
    elif command_text in COMMANDS_WITH_ARGS:
        return COMMANDS_WITH_ARGS[command_text](command_text, command_args)
    else:
        return commands.HelpCommand(error_message="I'm sorry, but I don't know what that means :-(")


def extract_task_num(command_args):
    if len(command_args) == 0:
        raise exceptions.TaskNumError("Please provide a task number. Format should be '[command] [task_num]'")
    if len(command_args) > 1:
        raise exceptions.TaskNumError("Please provide a valid task number. Format should be '[command] [task_num]'")
    try:
        task_num = int(command_args[0])
    except ValueError:
        raise exceptions.TaskNumError
    if task_num <= 0:
        raise exceptions.TaskNumError
    return task_num
