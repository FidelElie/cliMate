"""
"""
import os
import sys

from climate.lib import actions
from climate.lib import utilities
from climate.core import Menu, Help, Parsing,Settings
from climate.core.exceptions import ClimateArgumentError

MODULEPATH = str(os.path.abspath(os.path.dirname(__file__)))

class CliMate(object):
    """CliMate controls handlers and settings for the CliMate application.

    Parameters
    ----------
    cli: str, list, tuple, dict
        Cli data for loading in cliMate commands into appliaction.
    settings_to_overwrite: dict, list, tuple
        Iterator containing settings to be modified.
    """
    _arguments = sys.argv
    _settings = None

    cl_help_mappers = {
        "--commands": "display_help",
        "--docs": "show_docs"
        }

    def __init__(self, cli, settings_to_overwrite = None):
        self._cli_data = utilities.resolve_cli_data(cli)
        self._settings_handler = Settings()

        # mapped methods - map for different case conventions.
        self.parseArgs = self.parse_args

        self.set_settings = self._settings_handler.set_settings
        self.setSettings = self._settings_handler.set_settings

        self.set_setting = self._settings_handler.set_setting
        self.setSetting = self._settings_handler.set_setting

        if settings_to_overwrite != None:
            self.set_settings(settings_to_overwrite)

    def parse_args(self):
        """Parse command line arguments into CliMate procedure."""
        self._settings = self._settings_handler.settings

        if len(self._arguments) <= 1 and self._settings["use_menu"]:
            menu_handler = Menu(self._cli_data, self._settings)
            menu_handler.open_main_menu()
        elif len(self._arguments) <= 1 and not self._settings["use_menu"]:
            help_handler = Help(self._cli_data, self._settings).help_error()
        elif self._arguments[1] == "help":
            self.parse_help()
        else:
            parsing_handler = Parsing(
                self._arguments, self._cli_data, self._settings)
            parsing_handler.parse_data()

    def parse_help(self):
        """Parses arguments for help module of CliMate."""
        if len(self._arguments) > 2:
            cl_help_modifiers = [key for key in self.cl_help_mappers]
            if self._arguments[2] in cl_help_modifiers:
                help_handler = Help(self._cli_data, self._settings)
                help_command_str = self.cl_help_mappers[self._arguments[2]]
                help_command_method = getattr(help_handler, help_command_str)
                help_command_method()
            else:
                raise ValueError("Invalid optional command given for help.")
        elif self._settings["use_menu"]:
            if self._settings["docs_path"] != None:
                menuHandler = Menu(self._cli_data, self._settings)
                menuHandler.open_help_menu()
            else:
                help_handler = Help(self._cli_data, self._settings)
                help_command_str = self.cl_help_mappers["--commands"]
                help_command_method = getattr(help_handler, help_command_str)
                help_command_method()
        else:
            raise ValueError("No arguments given to help command.")

def main():
    cli_file = os.path.join(MODULEPATH, "cli.json")
    cli_settings = {
        "app_name": "CliMate",
        "docs_path": "www.github/fiddycodes/cliMate/README.md"
    }
    climate = CliMate(cli_file, cli_settings)
    climate.parse_args()
