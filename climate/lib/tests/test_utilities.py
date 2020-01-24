import os
import sys
import json
import unittest

from climate.lib import utilities

class TestUtilities(unittest.TestCase):
    def test_dict_to_rcd(self):
        """Testing dictionary being passed to resolve_cli_data function."""
        _dict = {
            "general": {},
            "commands": {}
            }

        self.assertEqual(
            utilities.resolve_cli_data(_dict),
            _dict,
            "Dictionary Passed Should Be Returned"
            )

    def test_file_to_rcd(self):
        """Testing file path being passed to resolve_cli_data function."""
        path = os.path.join("climate/lib/tests/data", "test_cli.json")
        with open(path, "r") as cli_file:
            json_contents = json.loads(cli_file.read())

        self.assertEqual(
            utilities.resolve_cli_data(path),
            json_contents,
            "Path To Json File, Should Return The Json Contents"
        )

    def test_files_to_rcd(self):
        """Testing mutliple files being passed to resolve_cli_data function."""
        file_names = ["test_general.json", "test_commands.json"]
        paths = [os.path.join("climate/lib/tests/data", name) for name in file_names]

        concecated_contents = {}
        for path in paths:
            with open(path, "r") as cli_file:
                concecated_contents.update(json.loads(cli_file.read()))

        self.assertEqual(
            utilities.resolve_cli_data(paths),
            concecated_contents,
            "Paths Json Files, Should Return Concecated Json Contents"
        )

    def test_write_json(self):
        """Testing the write_json function by writing a test file."""
        file_path = os.path.join("climate/lib/tests/data", "test_write.json")

        _data = {"value": "Test Data"}

        utilities.write_json(file_path, _data)

        self.assertTrue(os.path.isfile(file_path))

    def test_read_json(self):
        """Testing the read_json function by reading a test json file."""
        pass

    def test_read_data(self):
        """Testing the read_data function by reading a general file."""
        pass

    def test_get_entry(self):
        """Testing getting entry file using the get_entry function."""
        arguments = sys.argv
        base_entry = os.path.basename(arguments[0])

        self.assertEqual(
            utilities.get_entry(),
            base_entry,
            "Entries should be equal."
            )

    def test_add_space(self):
        """Testing bringing n size empty strings using add_space function."""
        test_string = "          " # 10 space string

        self.assertEqual(
            utilities.add_space(10),
            test_string,
            "Spaces in string equal should be equal to test string."
        )

if __name__ == "__main__":
    unittest.main()
