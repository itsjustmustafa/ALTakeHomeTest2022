"""
The DataFile API, responsible for manipulating and querying DataFrames within DataFiles.
This is the M in MVC.
This uses a Pandas DataFrames as the DataFrame implementation.
"""


import pandas as pd
from dataFileIO import DataFileIO
from dataFileIOCSV import DataFileIOCSV, InvalidFileType


class DataFile:
    def __init__(self, IO_handler):
        """
        Create a DataFile object.

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
        (based on Pandas' from_csv method)

        :param filename: The filename for the csv data
        :type filename: string
        :return: DataFile with datasource as the csv file `filename`
        :rtype: DataFile
        """
        IO_handler = DataFileIOCSV(filename)
        return DataFile(IO_handler)

    def get(self):
        """
        Get a deep copy of `_dataframe`.

        :return: A deep copy of the current dataframe
        :rtype: Pandas DataFrame
        """
        return self._dataframe.copy()

    def get_filename(self):
        """
        Get filename of DataFile from `_IO_handler`

        :return: filename
        :rtype: string
        """
        return self._IO_handler.get_filename()

    def save(self):
        """
        Save `_dataframe` to its source
        """
        self._IO_handler.save(self.get())

    def add_row(self, row):
        """
        Adds row `row` to `_dataframe`.

        :param row: Either a list of values or a dict representing the key/values for the new row
        :type row: dict or list
        """
        self._dataframe.loc[len(self._dataframe)] = row

    def remove_row(self, index, reset_index=True):
        """
        Remove a row (or a multiple rows) at a given index (or indices) from `_dataframe`.

        :param index: either a single index, or a list of indices
        :param reset_index: (default = True), will reset the index after the rows are removed
        :type index: int or list of ints
        :type reset_index: boolean
        """

        self._dataframe.drop(index, inplace=True)
        if reset_index:
            self._dataframe.reset_index(drop=True, inplace=True)

    def search(self, term, key, exact=True, search_df=None):
        """
        Searches each row of `_dataframe` for `term` in the column `key`.
        Exact search if `exact`, otherwise substring search.

        :param term: The string to search for in the `_dataframe`
        :param key: The column in `_dataframe` in which to search for `term`
        :param exact: (default True) If True, only return rows where values in `key` are exactly `term`, if False, return rows where `term` is a substring of values in `key`
        :param search_df: (defalt None) The dataframe to search within, if None, defaults to self._dataframe
        :type term: string
        :type key: string
        :type exact: boolean
        :type search_df: None or Pandas DataFrame
        :return: DataFrame with rows from `_dataframe` with only rows where `key` value is exactly `term`
        :rtype: Pandas DataFrame
        """
        try:

            if search_df is None:
                search_df = self._dataframe

            if exact:
                return search_df[search_df[key] == term].copy()
            else:
                return search_df[search_df[key].str.contains(term)].copy()

        except KeyError:
            raise KeyError("key={} not in this DataFrame".format(key))
        except Exception as e:
            raise e

    def search_multi(self, search_args, current_result=None):
        """
        Executes multiple search queries on the dataframe using recursion.

        :param search_args: List of search arguments (each elememnt is [term, key, exact])
        :param current_result: (default=None) The current search result to continue searching, if None then defaults to `_dataframe`
        :type search_args: List (each element is [string, string, boolean])
        :type current_result: None or Pandas DataFrame
        :return: Final result of the multiple searches
        :rtype: Pandas DataFrame
        """

        if current_result is None:
            current_result = self._dataframe.copy()

        if len(search_args) == 0:
            return current_result

        if len(current_result) == 0:
            return current_result

        term, key, exact = search_args[0]

        next_result = self.search(term, key, exact, search_df=current_result)

        return self.search_multi(search_args[1:], next_result)

    def change_row(self, row, index):
        """
        Changes the row at position `index` to `row`

        :param row: The replacement row to be placed at `index`
        :param index: The index of the row to be changed
        :type row: list or dict
        :type index: int
        """
        if index in range(len(self._dataframe)):
            self._dataframe.loc[index] = row
        else:
            raise IndexError(
                "Index {} out of bounds for DataFrame of length {}".format(
                    index, len(self._dataframe)
                )
            )

    def __len__(self):
        """
        Implementation of length, based on length of `_dataframe`

        :return: length of `_dataframe`
        :rtype: int
        """
        return len(self._dataframe)
