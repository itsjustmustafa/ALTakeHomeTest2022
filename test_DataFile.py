import pandas as pd
from dataFile import DataFile
from dataFileIO import DataFileIO
import unittest
from unittest.mock import MagicMock


class TestModel(unittest.TestCase):
    """
    Tests the DataFile class
    """

    def test_datafile_get(self):

        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob"],
                "Favourite Tea": ["Green", "English Breakfast"],
                "Favourite Number": ["7", "100"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        self.assertTrue(dataframe.equals(test_datafile.get()))

    def test_datafile_add_row(self):

        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob"],
                "Favourite Tea": ["Green", "English Breakfast"],
                "Favourite Number": ["7", "100"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        test_datafile.add_row(
            {"Name": "Charlie", "Favourite Tea": "Matcha", "Favourite Number": "9"}
        )

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )

        self.assertTrue(modified_dataframe.equals(test_datafile.get()))

    def test_datafile_remove_row_single(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        test_datafile.remove_row(1)

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Charlie"],
                "Favourite Tea": ["Green", "Matcha"],
                "Favourite Number": ["7", "9"],
            }
        )

        self.assertTrue(modified_dataframe.equals(test_datafile.get()))

    def test_datafile_remove_row_multi(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        test_datafile.remove_row([0, 1])

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Charlie"],
                "Favourite Tea": ["Matcha"],
                "Favourite Number": ["9"],
            }
        )

        self.assertTrue(modified_dataframe.equals(test_datafile.get()))

    def test_datafile_search_exact_nonempty(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        result_dataframe = test_datafile.search("Bob", "Name", exact=True)

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Bob"],
                "Favourite Tea": ["English Breakfast"],
                "Favourite Number": ["100"],
            }
        )

        modified_dataframe = modified_dataframe.set_index(pd.Index([1]))

        self.assertTrue(modified_dataframe.equals(result_dataframe))

    def test_datafile_search_exact_empty(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        result_dataframe = test_datafile.search("Hannah", "Name", exact=True)

        self.assertEqual(len(result_dataframe), 0)

    def test_datafile_search_substr_nonempty(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        result_dataframe = test_datafile.search("li", "Name", exact=False)

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Charlie"],
                "Favourite Tea": ["Green", "Matcha"],
                "Favourite Number": ["7", "9"],
            }
        )

        modified_dataframe = modified_dataframe.set_index(pd.Index([0, 2]))

        self.assertTrue(modified_dataframe.equals(result_dataframe))

    def test_datafile_search_substr_empty(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        result_dataframe = test_datafile.search("z", "Favourite Tea", exact=False)

        self.assertEqual(len(result_dataframe), 0)

    def test_datafile_search_invalid_key(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        result_dataframe = test_datafile.search("z", "Favourite Tea", exact=False)

        self.assertRaises(KeyError, test_datafile.search, "Sydney", "City")

    def test_datafile_search_multi_nonempty(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "9", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        search_terms = [["li", "Name", False], ["9", "Favourite Number", True]]

        result_dataframe = test_datafile.search_multi(search_terms)

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Charlie"],
                "Favourite Tea": ["Matcha"],
                "Favourite Number": ["9"],
            }
        )
        modified_dataframe = modified_dataframe.set_index(pd.Index([2]))

        self.assertTrue(modified_dataframe.equals(result_dataframe))

    def test_datafile_search_multi_invalid_key(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob", "Charlie"],
                "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
                "Favourite Number": ["7", "100", "9"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        search_terms = [["Sydney", "City", False], ["9", "Favourite Number", True]]

        self.assertRaises(KeyError, test_datafile.search_multi, search_terms)

    def test_change_row_valid_index(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob"],
                "Favourite Tea": ["Green", "English Breakfast"],
                "Favourite Number": ["7", "100"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        test_datafile.change_row(
            {"Name": "Charlie", "Favourite Tea": "Matcha", "Favourite Number": "9"}, 0
        )

        modified_dataframe = pd.DataFrame(
            {
                "Name": ["Charlie", "Bob"],
                "Favourite Tea": ["Matcha", "English Breakfast"],
                "Favourite Number": ["9", "100"],
            }
        )

        self.assertTrue(modified_dataframe.equals(test_datafile.get()))

    def test_change_row_invalid_index(self):
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)

        dataframe = pd.DataFrame(
            {
                "Name": ["Alice", "Bob"],
                "Favourite Tea": ["Green", "English Breakfast"],
                "Favourite Number": ["7", "100"],
            }
        )
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)

        invalid_index = 5
        altered_row = {
            "Name": "Charlie",
            "Favourite Tea": "Matcha",
            "Favourite Number": "9",
        }

        self.assertRaises(
            IndexError, test_datafile.change_row, altered_row, invalid_index
        )


if __name__ == "__main__":
    unittest.main()
