import unittest
from climate.lib.converters import map_int, map_float, map_bool, map_list

class TestConverters(unittest.TestCase):
    def test_map_int(self):
        self.assertEqual(map_int("1"), 1, "Should be 1")

    def test_map_float(self):
        self.assertEqual(map_float("1"), 1.0, "Should be 1.0")

    def test_map_bool(self):
        self.assertEqual(map_bool("True"), True, "Should be True")

    def test_map_list(self):
        data_types = ["int", "int", "int", "int"]
        self.assertEqual(map_list("[1, 4, 7, 10]", data_types), [1, 4, 7, 10])

    def test_map_list_varied_data(self):
        varied_data_types = ["int", "float", "float", "bool"]
        self.assertEqual(map_list("[1, 5, 4, True]", varied_data_types),
            [1, 5.0, 4.0, True])

if __name__ == "__main__":
    unittest.main()
