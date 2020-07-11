"""
"""
import sys

from climate.lib.converters import CONVERSION_TABLE
from climate.lib.converters import map_int, map_float, map_bool, map_list

class Parsing(object):
    """CliMate Parsing Handler for manipulating command line arguments.

    Parameters
    ----------
    arguments: list
        Arguments passed through by sys.argv.
    cli_data: dict
        Cli data passed through from main CliMate class.
    settings: dict
        CliMate settings passed through from main CliMate class.
    """

    def __init__(self, arguments, cli_data, settings):
        self.arguments = arguments
        self.cli_data = cli_data
        self.settings = settings

    def parse_data(self):
        commands = self.cli_data["commands"]
        chosen_command = commands[self.arguments[1]]

        command_arguments = chosen_command["arguments"]
        resolved_arguments = self.resolve_command_arguments(
            command_arguments, self.cli_data)

        dict_arguments = {key:None for key in resolved_arguments}

        keys = [*dict_arguments]
        for i, arg in enumerate(self.arguments[2:len(self.arguments)]):
            dict_arguments[keys[i]] = arg

        arg_data_types = [
            resolved_arguments[arg]["type"] for arg in keys]

        # check for missing data
        for i, key in enumerate(dict_arguments):
            if dict_arguments[key] == None:
                if "default" in resolved_arguments[key]:
                    dict_arguments[key] = resolved_arguments[key]["default"]
                else:
                    raise Exception("Required arguments missing")
            else:
                if arg_data_types[i] == "list":
                    values = [
                        dict_arguments[key], resolved_arguments[key]["map"]]
                else:
                    values = [dict_arguments[key]]
                dict_arguments[key] = \
                    CONVERSION_TABLE[arg_data_types[i]](*values)

        self.call_target(
            self.arguments[1], chosen_command["target"], dict_arguments, self.settings)

    @staticmethod
    def call_target(command_name, target, arguments, settings):
        """Resolves target and passes arguments to it.

        Parameters
        ----------
        command_name: str
            Name of command chosen by user.
        target: dict
            Dictionary conatining information regarding the object to call.
        arguments: dict
            Parameters to be parsed to the target.
        settings: dict
            Climate settings passed to function.
        """
        revised_arguments = {}
        for arg in arguments:
            revised_arguments[arg.replace("-", "_")] = arguments[arg]

        if "module-name" in target:
            if target["module-name"] in sys.modules:
                module = sys.modules.get(target["module-name"])
            else:
                raise ImportError("Error importing '{}' was not found.".format(
            target["module-name"]))
        else:
            module = sys.modules.get("__main__")

        try:
            return_obj = \
                lambda x: getattr(module, target[f"{x}-name"]) if f"{x}-name" in target else getattr(module, command_name.replace("-", "_"))

            _object = return_obj(target["type"])

            if target["type"] == "method":
                _object = getattr(module, target["class-name"])
                class_obj = _object
                instantiated_class = class_obj()
                _object = getattr(instantiated_class, target["method-name"])
        except KeyError:
            raise KeyError("No target type was given.")

        if arguments:
            if not settings["pass_by_dict"]:
                list_arguments = [revised_arguments[key] for key in revised_arguments]
                _object(*list_arguments)
            else:
                _object(**revised_arguments)
        else:
            _object()

    @staticmethod
    def resolve_command_arguments(command_arguments, cli_data) -> dict:
        """Resolve general arguments through their argument mappings.

        Parameters
        ----------
        command_arguments: dict
            Arguments from a chosen command.
        cli_data: dict
            The desired cli_data object for comparison.

        Returns
        -------
        resolved_arguments: dict
            Resolved Arguments from general arguments field are added.
        """
        resolved_arguments = command_arguments.copy()
        for args in resolved_arguments:
            argument = resolved_arguments[args]

            if isinstance(argument, str):
                try:
                    resolved_arguments[args] = \
                        cli_data["general"]["arguments"][argument]
                except KeyError:
                    raise KeyError(f"Argument string '{argument}' does not correspond to a general argument")
            elif isinstance(argument, dict):
                if "inherits" in argument:
                    inherited_arg = argument["inherits"]
                    res_arg = cli_data["general"]["arguments"][inherited_arg]
                    if "arguments" in argument:
                        arguments_to_overwrite = argument["arguments"]
                        res_arg.update(arguments_to_overwrite)
                    else:
                        # arguments need to be present for inheritance
                        raise Exception("No arguments present to be inherited, use standard argument")
                    resolved_arguments[args] = res_arg
                else:
                    continue
            else:
                raise TypeError("Mapping Only Supports Strings and Dicts")

        return resolved_arguments
