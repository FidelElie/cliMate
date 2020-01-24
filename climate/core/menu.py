"""
"""
import sys
import itertools

from climate.lib import mapper
from climate.lib import utilities
from climate.lib import inquirers
from climate.lib.inquirers import INQUIRER_TABLE
from climate.lib.converters import CONVERSION_TABLE
from climate.lib.converters import map_int, map_float, map_bool, map_list

from . import Parsing
from . import Help

class Menu(object):
    """Class For Handling Application Menu Navigation
    Will be disabled if the setting 'use_menu' is set to false

    Parameters
    ----------
    cli_data: dict
        Cli data passed through from main CliMate class.
    """
    current_local = []
    locations = []

    help_mapper = {
        "Show Commands": "display_help",
        "Show Documentation": "show_docs"
    }
    standard_option_mapper = {
        "Help": "open_help_menu",
        "Exit": "exit_application"
    }

    def __init__(self, cli_data, settings):
        self.cli_data = cli_data
        self.settings = settings

    def open_main_menu(self):
        if "menu" not in self.cli_data:
            self.standard_navigation()
        else:
            self.locations = self.cli_data["menu"]
            self.menued_navigation()

    def standard_navigation(self):
        commands = self.cli_data["commands"]
        command_keys = [key for key in commands]
        command_names = [commands[key]["name"] for key in commands]

        menu_names = command_names.copy()
        menu_names += self.add_menu_options()

        app_name = self.settings["app_name"]
        menu_message = app_name if app_name is not None else "Main Menu"

        command_menu_name = inquirers.inquirer_list(
            menu_names, menu_message, self.settings["style_data"])

        if command_menu_name in command_names:
            command_name_index = command_names.index(command_menu_name)
            command_key = command_keys[command_name_index]

            command_args = commands[command_key]["arguments"]
            parsed_command_args = \
                Parsing.resolve_command_arguments(
                    command_args, self.cli_data)
            command_target = commands[command_key]["target"]

            command_arguments = self.menu_arguments(parsed_command_args)
            Parsing.call_target(
                command_key, command_target, command_arguments, self.settings)
        else:
            # standard application option was chosen (i.e one not in cli file)
            method_string = self.standard_option_mapper[command_menu_name]
            getattr(self, method_string)()

    def menued_navigation(self):
        while True:
            command_found = False
            if not self.current_local:
                local = self.locations
            else:
                local = self.resolve_local(self.current_local)

            if isinstance(local, dict):
                local_func, local_args = inquirers.get_inquirer("list")
                local_args["list"] = local
                if self.current_local:
                    local["Back"] = "navigate_back"
                    local_args["message"] = self.current_local[-1]
                else:
                    # add buttons to main menu
                    for key in self.standard_option_mapper:
                        if self.settings[f"menu_{key.lower()}"]:
                            local[key] = self.standard_option_mapper[key]

                    app_name = self.settings["app_name"]
                    local_args["message"] = \
                        app_name if app_name is not None else "Main Menu"

                nav_point = local_func(**local_args)
                self.current_local += [nav_point]
            elif isinstance(local, str):
                try:
                    self.navigate_back()
                    if local not in [*self.cli_data["commands"]]:
                        command_found = True
                        getattr(self, local)()
                    else:
                        command_found = True
                        chosen_comamnd = self.cli_data["commands"][local]
                        command_target = chosen_comamnd["target"]

                        args = chosen_comamnd["arguments"]
                        resolved_arguments = \
                            ParsingHandler.resolve_command_arguments(args)
                        arguments = self.menu_arguments(resolved_arguments)
                        ParsingHandler.call_target(command_target, arguments)
                except KeyError:
                    TypeError("Error in chosen command.")
            else:
                raise TypeError("Invalid Datatype Found For Menu Navigation.")

            if command_found:
                if self.settings["exit_upon_command"]:
                    self.exit_applicaiton()

    def open_help_menu(self):
        help_func, help_args = inquirers.get_inquirer("choices")
        help_args["choices"] = [key for key in self.help_mapper]

        message = self.settings["help_menu_message"]
        help_args["message"] = message if message is not None else "Help"

        help_choice = help_func(**help_args)

        help_handler = Help(self.cli_data, self.settings)
        help_method_string = self.help_mapper[help_choice]
        getattr(help_handler, help_method_string)()

    def exit_applicaiton(self):
        print("Exiting Application")
        sys.exit(0)

    def add_menu_options(self):
        navigations = []
        for key in self.settings:
            if "menu" == key.split("_")[0]:
                navigations.append(
                    [self.settings[key], key.split("_")[1].capitalize()])

        return [nav[1] for nav in navigations if nav[0]]

    def resolve_local(self, keys):
        local = self.locations
        for key in keys:
            local = local[key]
        return local

    def navigate_back(self):
        del self.current_local[-1]

    @staticmethod
    def menu_arguments(command_args):
        """Uses Pyinquirer to get desired arguments through MenuHandler.

        Parameters
        ----------
        command_args: dict
            Dictionary containing the command arguments.

        Returns
        -------
        arguments: dict
            Dictionary containing desired and chosen arguments.
        """
        try:
            arguments = {}
            for arg in command_args:
                inquirer_function, inquirer_args = \
                    inquirers.get_inquirer(command_args[arg]["type"])

                inquirer_args["message"] = command_args[arg]["name"]

                if command_args[arg]["type"] == "choices":
                    if "map" in command_args[arg]:
                        inquirer_args["choices"] = \
                            mapper.map_string(
                                command_args[arg]["map"], arguments)
                    else:
                        inquirer_args["choices"] = \
                            [c for c in command_args[arg]["choices"].values()]

                    if "fallback" in command_args[arg]:
                        fallback_option = command_args[arg]["fallback"]
                        inquirer_args["choices"] += [fallback_option]

                        def fallback(x):
                            if x == command_args[arg]["fallback"]:
                                if "default" not in command_args[arg]:
                                    return None
                                else:
                                    return command_args[arg]["default"]

                        inquirer_args["lambda_filter"] = fallback

                arguments[arg] = inquirer_function(**inquirer_args)
        except KeyError:
            raise KeyError(f"Invalid Command argument '{arg}'")

        return arguments
