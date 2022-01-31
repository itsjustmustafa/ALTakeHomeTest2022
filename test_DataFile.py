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
        """
        Testing whether the get() method returns the same DataFrame as the input DataFrame, when nothing is modified
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob"],
            "Favourite Tea": ["Green", "English Breakfast"],
            "Favourite Number": ["7", "100"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())
        
        test_datafile = DataFile(test_IO)

        self.assertTrue(dataframe.equals(test_datafile.get()))
    
    def test_datafile_add_row(self):
        """
        Testing whether the add_row() method appends to the end of the DataFrame
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob"],
            "Favourite Tea": ["Green", "English Breakfast"],
            "Favourite Number": ["7", "100"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        test_datafile.add_row({"Name": "Charlie", "Favourite Tea": "Matcha", "Favourite Number": "9"})
        
        modified_dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        
        self.assertTrue(modified_dataframe.equals(test_datafile.get()))
        
    def test_datafile_remove_row_singular(self):
        """
        Testing whether the remove_row() method removes a single specified row of the DataFrame
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        test_datafile.remove_row(1)
        
        modified_dataframe = pd.DataFrame({
            "Name": ["Alice", "Charlie"],
            "Favourite Tea": ["Green", "Matcha"],
            "Favourite Number": ["7", "9"]
        })
        
        self.assertTrue(modified_dataframe.equals(test_datafile.get()))
    
    def test_datafile_remove_row_multiple(self):
        """
        Testing whether the remove_row() method removes a single specified row of the DataFrame
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        test_datafile.remove_row([0, 1])
        
        modified_dataframe = pd.DataFrame({
            "Name": ["Charlie"],
            "Favourite Tea": ["Matcha"],
            "Favourite Number": ["9"]
        })
        
        self.assertTrue(modified_dataframe.equals(test_datafile.get()))
    
    def test_datafile_search_exact_nonempty(self):
        """
        Testing whether the search() method finds a nonempty set of rows for a valid exact search
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        result_dataframe = test_datafile.search("Bob", "Name", exact=True)
        
        modified_dataframe = pd.DataFrame({
            "Name": ["Bob"],
            "Favourite Tea": ["English Breakfast"],
            "Favourite Number": ["100"]
        })
        
        modified_dataframe = modified_dataframe.set_index(pd.Index([1]))
        
        self.assertTrue(modified_dataframe.equals(result_dataframe))
    
    def test_datafile_search_exact_empty(self):
        """
        Testing whether the search() method returns an empty DataFrame on a bad exact search
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        result_dataframe = test_datafile.search("Hannah", "Name", exact=True)
        
        self.assertEqual(len(result_dataframe), 0)

    
    def test_datafile_search_substr_nonempty(self):
        """
        Testing whether the search() method finds a nonempty set of rows for a valid substring search
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        result_dataframe = test_datafile.search("li", "Name", exact=False)
        
        modified_dataframe = pd.DataFrame({
            "Name": ["Alice", "Charlie"],
            "Favourite Tea": ["Green", "Matcha"],
            "Favourite Number": ["7", "9"]
        })
        
        modified_dataframe = modified_dataframe.set_index(pd.Index([0, 2]))
        
        self.assertTrue(modified_dataframe.equals(result_dataframe))
    
    def test_datafile_search_substr_empty(self):
        """
        Testing whether the search_substr() method returns an empty DataFrame on a bad substring search
        """
        test_IO = DataFileIO()
        test_IO.save = MagicMock(return_value=None)
        
        dataframe = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Favourite Tea": ["Green", "English Breakfast", "Matcha"],
            "Favourite Number": ["7", "100", "9"]
        })
        test_IO.load = MagicMock(return_value=dataframe.copy())

        test_datafile = DataFile(test_IO)
        
        result_dataframe = test_datafile.search("z", "Favourite Tea", exact=False)
        
        self.assertEqual(len(result_dataframe), 0)

if __name__ == '__main__':
    unittest.main()