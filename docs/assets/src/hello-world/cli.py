from climate import CliMate
from core import actions

if __name__ == "__main__":
    climate = CliMate("cli.json")
    climate.parse_args()
