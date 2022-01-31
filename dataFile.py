import pandas as pd
from dataFileIO import DataFileIO
from dataFileIOCSV import DataFileIOCSV

class DataFile():
    """
    DataFile is a data querying API that uses a Pandas DataFrame
    """
    
    def __init__(self, IO_handler):
        """
        :param IO_handler: The file handler that takes care of saving and loading
        :type IO_handler: DataFileIO
        """
        self._IO_handler = IO_handler
        self._dataframe = self._IO_handler.load()
     
    @staticmethod
    def from_csv(filename):
        """
        Returns a DataFile using a csv file as a source.
        Creates a DataFileIOCSV as an IO_handler for the DataFile.
        :param filename: The filename for the csv data
        :type filename: string
        :return: DataFile with datasource as the csv file `filename`
        :rtype: DataFile
        """        
        IO_handler = DataFileIOCSV(filename)
        return DataFile(IO_handler)
     
    def add_row(self, row):
        """
        This function will append a row to the end of `_dataframe`.
        :param row: Either a list of values or a dict representing the key/values for the new row
        :type row: dict or list
        """
        self._dataframe.loc[len(self._dataframe)] = row
        
    def remove_row(self, index, reset_index = True):
        """
        This function will remove a row at a given index from `_dataframe`.
        :param index: either a single index, or a list of indices
        :param reset_index: (default = True), will reset the index after the rows are removed
        :type index: int or list of ints
        :type reset_index: boolean
        """
        self._dataframe = self._dataframe.drop(index)
        if reset_index:
            self._dataframe.reset_index(drop=True, inplace=True)
        
    def get(self):
        """
        This function will return a deep copy of `_dataframe`.
        :return: A deep copy of the current dataframe
        :rtype: Pandas DataFrame      
        """
        return self._dataframe.copy()
    
    def search(self, term, key, exact=True):
        """
        Searches each row of `_dataframe` for `term` in the column `key`.
        Exact search if `exact`, otherwise substring search.
        :param term: The string to search for in the `_dataframe`
        :param key: The column in `_dataframe` in which to search for `term`
        :param exact: (default True) If True, only return rows where values in `key` are exactly
                      `term`, if False, return rows where `term` is a substring of values in `key`
        :type term: string
        :type key: string
        :type exact: boolean
        :return: DataFrame with rows from `_dataframe` with only rows where `key` value is exactly `term`
        :rtype: Pandas DataFrame
        """
        try:
            if exact:
                return self._dataframe[self._dataframe[key] == term].copy()
            else:
                return self._dataframe[self._dataframe[key].str.contains(term)].copy()
        except KeyError:
            raise KeyError("key={} not in this DataFrame".format(key))
        except Exception as e:
            raise e()
    
    def save(self):
        """
        This function will save `_dataframe` to the 
        """
        self._IO_handler.save(self.get())
    
    