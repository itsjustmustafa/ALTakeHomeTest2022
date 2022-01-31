import pandas as pd
from dataFileIO import IO

class DataFile():
    """
    This is the main API that uses a Pandas dataframe as the medium for data   
    """
    def __init__(self, IO_handler):
    
        self._IO_handler = IO_handler
        self._dataframe = self._IO_handler.load()
        
    def add_row(self, row):
        """
        This function will append a row to the end of DataFile._dataframe
        :param row: Either a list of values or a dict representing the key/values for the new row
        """
        self._dataframe.loc[len(self._dataframe)] = row
        
    def remove_row(self, index, reset_index = True):
        """
        This function will remove a row at a given index from DataFile._dataframe
        :param index: either an integer for the index of the row, or a list of integers for multiple indices (integer)
        :param reset_index: will reset the index of the Pandas Dataframe after all the rows to remove are removed
        """
        self._dataframe = self._dataframe.drop(index)
        if reset_index:
            self._dataframe.reset_index(drop=True, inplace=True)
        
    def get(self):
        """
        This function will return a deep copy of DataFile._dataframe
        :return: Pandas DataFrame
        """
        return self._dataframe.copy()
        
    def save(self):
        """
        This function will save  DataFile._dataframe
        """
        self._IO_handler.save(self.get())
    