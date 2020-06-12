from duke import parser

INDENTED_HORIZONTAL_LINE = "\t" + ("_" * 80)
COMMANDS = [command for command in parser.COMMANDS_WITH_ARGS] + [command for command in parser.COMMANDS_WITH_NO_ARGS]
HELP_TEXT = "Commands:\n\t" + "\n\t".join(command for command in COMMANDS)


def prepend_tab(text):
    text_lines = text.split("\n")
    tabbed_lines = ["\t" + line for line in text_lines]
    tabbed_text = "\n".join(tabbed_lines)
    return tabbed_text


def output_text(*text_args, display_help_text=False):
    print(INDENTED_HORIZONTAL_LINE)
    for text in text_args:
        print(prepend_tab(text))
    if display_help_text:
        if len(text_args) > 0:
            print()
        print(prepend_tab(HELP_TEXT))
    print(INDENTED_HORIZONTAL_LINE)


def output_help_text():
    output_text(display_help_text=True)


def greet():
    output_text("Hello! I'm Duke's friend, Python!\n"
                "What can I do for you?")


def say_goodbye():
    output_text("Bye. Hope to see you again soon!")


def unrecognised_command():
    output_text("I'm sorry, but I don't know what that means :-(")


def output_error(message, display_help_text=False):
    output_text("☹ OOPS!!! " + message, display_help_text=display_help_text)


def show_loading_text():
    output_text("Loading task list from file...")


def show_successful_load_text():
    output_text("Successfully loaded file.")


def show_failed_load_text(message):
    output_error(message + "\nCreating task list from scratch.")
