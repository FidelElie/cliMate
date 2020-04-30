"""
"""
class Settings(object):
    """Handles Settings For CliMate.

    Settings
    --------
    use_menu: bool
        Determines whether CliMate application has a menu. True by default.
    docs_path: str
        Sets path to application documentation, either a url or file path
    app_name: str
        Sets desired application name, to be displayed in main menu.
    menu_help: bool
        Determines whether 'Help' option is added to standard menu (When no menu is present in cli.json file). Will have no affect if 'use_menu' settings is set to False. True by default.
    menu_exit: bool
        Determines whether 'Exit' option is added to standard menu (When no menu is present in cli.json file). Will have no affect is 'use_menu' settings is set to False. True by default.
    pass_by_dict: bool
        Determines if instead of passing arguments through list unpacking (*arguments), dictionary unpacking (**arguments) is used. False by Default.
    help_menu_message: str
        Sets message that is displayed on the help sub menu.
    exit_upon_command: bool
        Sets whether the application will exit after completing command or it will loop back to where the user was in the menu hierarchy. This setting only takes affect if 'menu' field is present in cli as well as the 'use_menu' setting being set to True.
    """
    settings = {
        "use_menu": True,
        "docs_path": None,
        "app_name": None,
        "menu_help": True,
        "menu_exit": True,
        "pass_by_dict": False,
        "help_menu_message": None,
        "exit_upon_command": True
    }

    def set_setting(self, key, value):
        """Set a singular setting for CliMate application.

        Parameters
        ----------
        key: str
            Key corresponding to setting value.
        value: str, bool
            Value to set settings to.
        """
        self.change_setting(key, value)

    def set_settings(self, iterator):
        """Set multiple settings for CliMate application using iterator.

        Parameters
        ----------
        iterator: list, dict, tuple
            Iterator containing keys and their desired corresponding values.
        """
        if isinstance(iterator, dict):
            for key in iterator:
                self.change_setting(key, iterator[key])
        elif isinstance(iterator, (list, tuple)):
            try:
                for setting in iterator:
                    self.change_setting(setting[0], setting[1])
            except IndexError:
                raise IndexError("Formatting Issue In Settings Iterator")
        else:
            raise TypeError("Iterator of type Dict, List And Tuple Expected got {}".format(type(iterator).__name__))

    def change_setting(self, key, value):
        """Change a setting value in the settings dicionary.

        Parameters
        ----------
        key: str
            Key corresponding to setting value.
        value: str, bool
            Value to set settings to.
        """
        if key in self.settings:
            if isinstance(self.settings[key], bool):
                if isinstance(value, bool):
                    self.settings[key] = value
                else:
                    raise TypeError("Boolean value expected got type {}".format(type(value).__name__))
            elif self.settings[key] is None:
                self.settings[key] = value
            else:
                raise TypeError("No type given for settings key.")
        else:
            raise Exception(f"Key not found in settings got {key}")
