from climate import CliMate


def say_hello(name):
    print("Hello, {}!".format(name))


if __name__ == "__main__":
    climate = CliMate("tests/core/cli.json")
    climate.parse_args()
