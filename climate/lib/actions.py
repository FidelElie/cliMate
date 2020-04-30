"""
"""
import os
import json

from . import utilities
from . import data

def new_application(cli_dir: str, path_commands: bool):
    """Creates new cli applicaiton, creates the cli.json file.

    Parameters
    ----------
    cli_dir: str
        Dir path to where the cli.json file should be created.
    path_commands: bool
        Whether the calls field should be added to the cli.json file.
    """
    if cli_dir is not "":
        if not os.path.isdir(cli_dir):
            os.makedirs(cli_dir)

    json_path = os.path.join(cli_dir, "cli.json")
    python_path = os.path.join(cli_dir, "cli.py")

    if path_commands:
        path_command = {"calls": []}
        cli_contents["general"].update(path_command)

    cli_contents["general"].update({"arguments": {}})

    utilities.write_json(json_path, data.CLI_CONTENT.copy())
    utilities.write_data(python_path, data.PYTHON_CONTENT)

    print("CliMate App Created In {}".format(
        "Root" if cli_dir is "" else cli_dir))

def new_command(cli_path: str, arg_amount: int, target_type: str):
    """Add a new command to the cli.json file.

    Parameters
    ----------
    cli_path: str
        Path to the cli.json file.
    arg_amount: int
        Number of arguments to add to the command.
    target_type: str
        Target data to add to the command.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find file: {}".format(cli_path))

    command_contents = data.COMMAND_CONTENT.copy()

    if target_type is not None:
        target = TARGETS[target_type]
    else:
        target = {}

    command_contents["target"] = target

    if arg_amount != 0:
        arguments = {}
        for i in range(arg_amount):
            arguments[f"new-argument-{i}"] = data.ARGUMENT_CONTENT.copy()

        command_contents["arguments"] = arguments

    # load existing cli.json file contents
    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]

    command_amount = len(cli_commands.keys())

    cli_commands[f"new-command-{command_amount + 1}"] = command_contents

    cli_present["commands"] = cli_commands

    utilities.write_json(cli_path, cli_present)

    print("New command added to Cli file {}".format(cli_path))

def new_argument(cli_path: str, command_name: str, arg_amount: int):
    """Add new argument(s) to existing command in cli.json file.

    Parameters
    ----------
    cli_path: str
        Path to the cli.json file.
    command_name: str
        Name of existing command in the cli.json file.
    arg_amount: int
        Number of arguments to add to the command.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find file: {}".format(cli_path))

    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]

    chosen_command = cli_commands[command_name]

    if arg_amount != 0:
        arguments_to_add = {}
        if "arguments" in chosen_command:
            current_arg_amount = len(chosen_command["arguments"])
        else:
            current_arg_amount = 0

        for i in range(arg_amount):
            arguments_to_add[
                f"new-argument-{i + current_arg_amount}"] = data.ARGUMENT_CONTENT.copy()
    else:
        raise ValueError("No number of arguments were added.")

    if "arguments" in chosen_command:
        arguments = chosen_command["arguments"]
        arguments.update(arguments_to_add)
        chosen_command["arguments"] = arguments
    else:
        chosen_command["arguments"] = arguments_to_add

    cli_commands[command_name] = chosen_command
    cli_present["commands"] = cli_commands

    utilities.write_json(cli_path, cli_present)

    print("New Argument added to command {}".format(command_name))

def new_general_argument(self, cli_path, arg_amount):
    """Add new general arguments to the cli.json file.

    cli_path: str
        Path to the cli.json file.
    arg_amount: int
        Number of arguments to add to the general arguments.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find Cli File: {}".format(cli_path))

    cli_present = utilities.read_json(cli_path)
    cli_general = cli_present["general"]

    new_general_argument = data.ARGUMENT_CONTENT.copy()
    if "arguments" not in cli_general:
        cli_general["arguments"] = {}

    current_arguments_numb = len(cli_general["arguments"].keys())

    for i in range(arg_amount):
        cli_general["arguments"][f"new-gen-arg-{current_arguments_numb + i + 1}"]

    cli_present["general"] = cli_general

    utilities.write_json(cli_path, cli_present)

    print("General Arguments added to Cli File.")

def remove_command(cli_path: str, command_name: str):
    """Remove existing command from the cli.json file.

    Parameters
    ----------
    cli_path: str
        Path to the cli.json file.
    command_name: str
        Name of existing command in the cli.json file.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find Cli file: {}".format(cli_path))

    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]

    if command_name in cli_commands:
        del cli_commands[command_name]
    else:
        raise KeyError(f"Could not find command '{command_name}'")

    cli_present.update(cli_commands)

    utilities.write_json(cli_path, cli_present)

    print("Command '{}' removed from Cli File".format(command_name))

def remove_argument(cli_path: str, command_name: str, argument_name: str):
    """Remove existing argument from existing command in cli.json file.

    Parameters
    ----------
    cli_path: str
        Path to the cli.json file.
    command_name: str
        Name of existing command in the cli.json file.
    argument_name: str
        Name of existing argument in a command in the cli.json file.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find Cli File: {}".format(cli_path))

    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]

    chosen_command = cli_commands[command_name]
    command_arguments = chosen_command["arguments"]

    if argument_name in command_arguments:
        del command_arguments[argument_name]
    else:
        raise KeyError(
    f"Could not find argument '{argument_name}' in Cli File")

    chosen_command["arguments"] = command_arguments
    cli_commands[command_name] = chosen_command
    cli_present.update(cli_commands)

    utilities.write_json(cli_path, cli_present)

    print("Argument '{}' removed from Command '{}' in Cli File".format(argument_name, command_name))

def add_menu(cli_path: str):
    """Add menu field to the cli.json file.

    Parameters
    ----------
    cli_path: str
        Path to the cli.json file.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find file: {}".format(cli_path))

    cli_present = utilities.read_json(cli_path)
    cli_present["general"]["menu"] = {}

    utilities.write_json(cli_path, cli_present)

    print("Menu field added to cli file")

def add_path_command(cli_path: str, setup_path: str):
    """Add path commands from module setup files.

    Parameters
    ----------
    cli_path: str
        Path to the cli.json file.
    setup_path: str
        Path to the setup.py file.
    """
    if not os.path.isfile(cli_path):
        raise FileNotFoundError("Could not find Cli File: {}".format(cli_path))

    if not os.path.isfile(setup_path):
        raise FileNotFoundError("Could not find Setup File: {}".format(setup_path))

    try:
        setup_contents = utilities.read_data(setup_path, "list")

        for i, line in enumerate(setup_contents):
            if "entry_points" in line:
                start_index = i
            if "}" in line and i >= start_index:
                end_index = i

        entry_points_list = setup_contents[start_index:end_index+1]
    except NameError:
        raise NameError("No entry points are present in setup file")
    else:
        cli_data = utilities.read_json(cli_path)
        general_dict_contents = cli_data["general"]
        if "calls" not in general_dict_contents:
            print("Creating script-command Field")
            scripts_commands = {"calls": path_scripts}
            general_dict_contents = {
                **scripts_commands, **general_dict_contents}
        else:
            print("Overwriting Existing Script Commands")
            general_dict_contents["calls"] = path_scripts

        cli_data["general"] = general_dict_contents

        utilities.write_json(cli_path, cli_data)
        print("Path commands added to Cli File")
