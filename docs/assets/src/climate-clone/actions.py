from climate import utilities
from climate import data

def new_application(cli_dir):
    utilities.check_cli_dir(cli_dir)
    json_path = utilities.join_path(cli_dir, "cli-test.json")
    python_path = utilities.join_path(cli_dir, "cli-test.py")
    utilities.write_json(json_path, data.CLI_CONTENTS.copy())
    utilities.write_data(python_path, data.PYTHON_CONTENT)
    local = "Root" if cli_dir is "" else cli_dir
    print(f"CliMate App Created In {local}")

def new_command(cli_path, arg_amount, target_type):
    utilities.check_cli_path(cli_path)
    command_contents = data.COMMAND_CONTENT.copy()
    target = targets[target_type] if target_type is not None else {}
    command_contents["target"] = target

    if arg_amount != 0:
        arguments = {}
        for i in range(arg_amount):
            arguments[f"new-arguments-{i}"] = data.ARGUMENT_CONTENT.copy()
        command_contents["arguments"] = arguments

    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]
    command_amount = len(cli_commands.keys())
    cli_commands[f"new-command-{command_amount + 1}"] = command_contents
    cli_present["commands"] = cli_commands
    utilities.write_json(cli_path, cli_present)
    print(f"New command added to Cli File {cli_path}")

def new_argument(cli_path, command_name, arg_amount):
    utilities.check_cli_path(cli_path)
    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]
    chosen_command = cli_commands[command_name]

    if arg_amount != 0:
        arguments_to_add = {}
        if "arguments" in chosen_command:
            current_arg_amount = len(chosen_command["arguments"].keys())
        else:
            chosen_command["arguments"] = {}
            current_arg_amount = 0

        for i in range(arg_amount):
            new_arg_number = i + current_arg_amount
            arguments_to_add[f"new-argument-{new_arg_number}"] = \
                data.ARGUMENT_CONTENT.copy()
    else:
        raise ValueError("No Number Of Arguments Were Added")

    arguments = chosen_command["arguments"]
    arguments.update(arguments_to_add)
    chosen_command["arguments"] = arguments
    cli_commands[command_name] = chosen_command
    cli_present["commands"] = cli_commands
    utilities.write_json(cli_path, cli_present)
    print(f"New argument added to command '{command_name}'")

def remove_command(cli_path, command_name):
    utilites.check_cli_path(cli_path)
    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]

    if commands_name in cli_commands:
        del cli_commands[command_name]
    else:
        raise KeyError(f"Could Not Find Command '{command_name}'")

    cli_present["commands"] = cli_commands
    utilities.write_json(cli_path, cli_present)
    print(f"Command '{command_name}' removed from Cli File {cli_path}")

def remove_argument(cli_path, command_name, argument_name):
    utilities.check_cli_path(cli_path)
    cli_present = utilities.read_json(cli_path)
    cli_commands = cli_present["commands"]
    chosen_command = cli_commands[command_name]
    command_arguments = chosen_command["arguments"]

    if argument_name in command_arguments:
        del command_arguments[argument_name]
    else:
        raise KeyError(f"Could not find '{argument_name}' in Cli File")

    chosen_command["arguments"] = command_arguments
    cli_commands[command_name] = chosen_command
    cli_present["commands"] = cli_commands
    utilities.write_json(cli_path, cli_present)
    print(f"Argument '{argument_name}' remove from command {command_name}")
