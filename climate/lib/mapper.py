"""
"""
import os
import re

from . import utilities

def get(content, identifier, filter_value):
    """Filter information from a content object.

    Parameters
    ----------
    content: list, dict
        The content to be filtered.
    identifier: str
        The method at which it should be filtered i.e through dictionary keys or through list indexes.
    filter_value: int, str
        The value to be filtered by.

    Returns
    -------
    value: str, list

    """
    try:
        if identifier == "line":
            value = content[filter_value]
        elif identifier == "keys":
            if "|" in filter_value:
                filters = [val.strip() for val in filter_value.split("|")]
                value = content.copy()
                for _filter in filters:
                    value = value[_filter]
                value = list(value.keys())
            else:
                value = list(content[filter_value].keys())
    except KeyError:
        raise KeyError("")
    except IndexError:
        raise IndexError("")

    return value

def read_file(path):
    """Read file data from a file path.

    Parameters
    ----------
    path: str
        Path to json file.

    Returns
    -------
    file_data: dict, list
        Data read from file.
    """
    try:
        file_name = os.path.basename(path)
        if ".json" in file_name:
            file_data = utilities.read_json(path)
        else:
            with open(path, "r") as read_file:
                file_data = read_file.readlines()
    except FileNotFoundError:
        raise FileNotFoundError("")
    except PermissionError:
        raise PermissionError("")

    return file_data

MAPPER_TABLE = {
    "get": get,
    "read": read_file
}

def map_string(string_map, arguments):
    """Use choice map string to fetch dynamic choice lists.

    Parameters
    ----------
    string_map: string
        String to be mapped to command operations.
    arguments: dict
        Command arguments that have already been parsed.

    Returns
    -------
    choice_value: list
        The list of choices to be dynamically used in CliMate menus.
    """
    string = string_map

    pulled_commands, stripped_commands = get_command_mappings(string)
    # remove any white space that could have been added by user
    for i, item in enumerate(pulled_commands):
        string = string.replace(pulled_commands[i], stripped_commands[i])

    for arg in arguments:
        string = string.replace(f"{arg}", str(arguments[arg]))

    commands = [remove_command_flag(s) for s in string.split(",")]

    try:
        returned_values = []
        for i, command in enumerate(commands):
            split_command = command.split()
            function_command = MAPPER_TABLE[split_command[0]]
            if split_command[0] == "get":
                del split_command[0]
                func_arguments = [returned_values[i - 1]] + split_command
            elif split_command[0] == "return_value":
                del split_command[0]
                current_commands = stripped_commands[0:i+1]
                value_indexes = [
                    j for j, d in enumerate(current_commands) if d == stripped_commands[i]]
                func_arguments = [returned_values[value_indexes[-2]]]
            else:
                del split_command[0]
                func_arguments = split_command
            returned_values.append(function_command(*func_arguments))
    except IndexError:
        raise IndexError("Get commands have to follow a command.")

    choice_value = returned_values[-1]

    return choice_value

def remove_command_flag(command_string):
    """Remove the command flags from a command string.

    Parameters
    ----------
    command_string: str
        String containing commands, incased in {}

    Returns
    -------
    translated_command: str
        Command with bracket flags removed.
    """
    brackets = ["{", "}"]
    trans_dict = {bracket:"" for bracket in brackets}
    translate = lambda x, trans: x.translate(str.maketrans(trans))
    translated_command = translate(command_string, trans_dict)

    return translated_command


def get_command_mappings(mapping_string):
    """Extract command maps from the command string.

    Parameters
    ----------
    mapping_string: str
        String containing mapping commands incased in {}.

    Return
    ------
    pulled_commands: list
        Commands stripped from mapping string.
    stripped_commands: list
        Commands stripped from mapping string with all whitespace removed.
    """
    pulled_commands = [x for x in re.findall('\{.*?\}', mapping_string)]
    stripped_commands = [x.replace(" ", "") for x in pulled_commands]

    return pulled_commands, stripped_commands
