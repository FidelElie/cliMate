"""
"""
import webbrowser

from climate.lib import mapper
from climate.lib import utilities

from . import Parsing

class Help(object):
    """CliMate help handler for parsing application help commands.

    Parameters
    ----------
    cli_data: dict
        Cli data passed through from main CliMate class.
    settings: dict
        CliMate settings passed through from main CliMate class.
    """
    help_command = {
        "help": {
            "name": "Get Help",
            "description": "Get help for the application.",
            "arguments": {
                "optional-help": {
                    "name": "Optional Commands",
                    "description": "Getting help through documentation or commands.",
                    "type": "choices",
                    "choices": {
                        "--docs": "Show Documentation",
                        "--commands": "Show Commands"
                    }
                }
            }
        }
    }

    def __init__(self, cli_data, settings):
        self.cli_data = cli_data
        self.settings = settings

    def help_error(self, message = None):
        """Displays error messages upon no command being provided. Method is disabled if 'use_menu' is set to True.

        Parameters
        ----------
        message: str
            Error message to be displayed when no values are provided
        """
        if message is not None:
            print(message)
        else:
            print("Error No Commands Were Given")
        print("\n")
        self.display_help()

    def show_docs(self):
        """Displays the documentation of the cli application."""
        if self.settings["docs_path"] is None:
            raise ValueError("No Documentation Path Or Url Provided")
        else:
            print("Opening Documentation")
            webbrowser.open(self.settings["docs_path"])

    def display_help(self):
        """Print command and argument information to the terminal."""
        # Print The Entry Command
        print("-Entry-")
        general = self.cli_data["general"]

        calls = general["calls"] if "calls" in general else []

        entry_filter = lambda x: "|".join(x) if x else utilities.get_entry()

        call_string = f"-{entry_filter(calls)}- [command] {{argument}}"

        print(f"{utilities.add_space(4)}{call_string}")

        # Print The Command Data
        print("[Command(s)]")

        arguments = {}
        commands = self.cli_data["commands"]
        commands.update(self.help_command)

        for command in commands:
            com_iden = command
            com_name = commands[command]["name"]
            com_desc = commands[command]["description"]
            com_arguments = commands[command]["arguments"]
            com_args = [f"{{{key}}}" for key in commands[command]["arguments"]]

            resolved_args = Parsing.resolve_command_arguments(
                com_arguments, self.cli_data)

            # overwites duplicate key values
            arguments.update(resolved_args)

            command_str = "{} {}".format(com_iden, " ".join(com_args))
            command_desc = "{}{}".format(utilities.add_space(8), com_desc)

            print(f"{utilities.add_space(4)}{command_str}\n{command_desc}")

        print("{Argument(s)}")
        for arg in arguments:
            arg_iden = arg
            arg_cont = arguments[arg]
            arg_name = arguments[arg]["name"]
            arg_desc = arguments[arg]["description"]
            arg_type = arguments[arg]["type"]

            if arg_type == "choices":
                if "choices" in arg_cont:
                    modifiers = [val for val in arg_cont["choices"]]

                    argument_str = "{} ({}) {}".format(
                        arg_iden, arg_type, "|".join(modifiers))
                elif "map" in arg_cont:
                    mappings = mapper.get_command_mappings(arg_cont["map"])
                    stripped_command = \
                        mapper.remove_command_flag(mappings[1][-1])
                    split_commands = stripped_command.split("|")
                    map_target = \
                        split_commands[-2] if len(split_commands) > 1 else split_commands[0]

                    argument_str = "{} ({}) --value taken from key '{}'.".format(arg_iden, arg_type, map_target)
                else:
                    raise Exception("No corresponding value key in choices")
            else:
                argument_str = "{} ({})".format(arg_iden, arg_type)

            argument_desc = "{}{}".format(utilities.add_space(8), arg_desc)
            print(f"{utilities.add_space(4)}{argument_str}\n{argument_desc}")
