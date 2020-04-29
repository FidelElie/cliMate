from climate import CliMate
from core import actions

if __name__ == "__main__":
    climate = CliMate("cli.json")
    climate.set_settings({
        "app_name": "CliMate",
        "docs_path": "https://fidelelie.github.io/cliMate/tutorials"
    })
    climate.parse_args()

