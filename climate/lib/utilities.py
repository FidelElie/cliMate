"""
"""
import os
import sys
import json

def resolve_cli_data(cli) -> dict:
    """Resolves Cli Data into a usable python dictionary.

    Parameters
    ----------
    cli: dict, str, tuple, list
        Cli data for loading in cliMate commands into application. Dictionaries are passthrough function unchanged. Strings are
        treated as file paths and lists and tuples are treated as a list
        of file paths.

    Returns
    -------
    cli_data: dict
        Cli data for use in the rest of the application. File paths are
        loaded and converted into the dictionaries.

    Examples
    --------
    >>> _dict = {"test_info": "data"}

    >>> data = resolve_cli_data(_dict)

    >>> # this will return the same dictionary.
    """
    if isinstance(cli, dict):
        cli_data = cli.copy()
    elif isinstance(cli, str):
        c = read_json(cli)
        cli_data = c.copy()
    elif isinstance(cli, (tuple, list)):
        cli_datas = [read_json(c) for c in cli]
        cli_data = {k: v for d in cli_datas for k, v in d.items()}
    else:
        raise TypeError(
    f"No Dict, List, String Or Tuple Given Got {type(cli).__name__}.")

    if "general" not in cli_data or "commands" not in cli_data:
        raise Exception("General Or Commands Field Missing From Cli File.")

    return cli_data

def write_json(path, contents, indent_amount = 4):
    """Write JSON data from dictionary to file object.

    Parameters
    ----------
    path: str
        Path to json file.
    contents: dict
        Dictionary content to be written to the file.
    indent_amount: int
        The amount to indent in the json file.
    """
    if not isinstance(contents, dict):
        raise TypeError("Invalid type for contents expected dict got {}".format(type(contents).__name__))

    with open(path, "w") as json_file:
        json.dump(contents, json_file, indent=indent_amount)

def write_data(path, contents):
    """Write data to a file object

    Parameters
    ----------
    path: str
        Path to file object.
    contents: str, list, tuple
        Content to be written to the file.
    """
    with open(path, "w") as data_file:
        data_file.write(contents)

    try:
        with open(path, "w") as data_file:
            if isinstance(contents, str):
                data_file.write(contents)
            elif isinstance(contents, (tuple, list)):
                data_file.write("\n".join(contents))
    except FileNotFoundError:
        raise FileNotFoundError(f"File Object Could Not Be Found at path {path}")

def read_json(path):
    """Read JSON data from file with corresponding custom exceptions.

    Parameters
    ----------
    path: str
        Path to json file.

    Returns
    -------
    json_data: dict
        Dictionary of data loaded from json file.
    """
    try:
        with open(path, "r") as json_file:
            json_data = json.loads(json_file.read())

    except json.JSONDecodeError:
        raise json.JSONDecodeError(
                f"File {os.path.basename(path)} Could Not be Loaded.")
    except FileNotFoundError:
        raise FileNotFoundError(
                f"File {os.path.basename(path)} Could Not Be Found.")
    except PermissionError:
        raise PermissionError(
    f"File {os.path.basename(path)} Could not be accessed, lack of permission.")

    return json_data

def read_data(path, modifier = "string"):
    """Read data from a file object.

    Parameters
    ----------
    path: str
        Path to file you want to be read.
    modifier: str
        Modifiers 'list' or 'string' for how the file should be read.

    Returns
    -------
    data: str
        Data from file object as either a string or list.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"")
    try:
        with open(path, "r") as _file:
            if modifier == "list":
                data = _file.readlines()
            else:
                data = _file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File To Be Loaded Could Not Be Found")

    return data

def get_entry():
    """Fetch the name of the file entry point.

    Returns
    -------
    base_entry: str
        Name of the entry file.
    """
    arguments = sys.argv
    base_entry = os.path.basename(arguments[0])

    return base_entry

def check_cli_dir(cli_dir):
    """Check If A Specified Cli Dir is Present

    Parameters
    ----------
    cli_dir: str
        Path To Cli Dir
    """
    if cli_dir is not "":
        if not os.path.isdir(cli_dir):
            os.makedirs(cli_dir)

def join_path(path1, path2):
    """ Join Two File Paths (Wrapper For Os Library)

    Parameters
    ----------
    path1: str
        First section of path
    path2: str
        Second section of path

    Returns
    -------
    joined_path: str
        Joined path
    """
    joined_path = os.path.join(path1, path2)
    return joined_path



