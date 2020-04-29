CLI_CONTENT = {
    "general": {},
    "commands": {}
}
COMMAND_CONTENT = {
    "name": "",
    "description": ""
}
ARGUMENT_CONTENT = {
    "name": "",
    "type": "",
    "description": ""
}
TARGETS = {
    "--function": {
        "type": "function",
        "module-name": "",
        "function-name": ""
    },
    "--class": {
        "type": "class",
        "module-name": "",
        "class-name": ""
    },
    "--method": {
        "type": "method",
        "module-name": "",
        "class-name": "",
        "method-name": ""
    }
}

PYTHON_CONTENT = \
    """
from climate import CliMate

if __name__ == "__main__":
    climate = CliMate("cli.json")
    climate.parse_args()
"""
