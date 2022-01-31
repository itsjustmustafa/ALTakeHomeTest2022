import pandas as pd
from modelIO import IO

class DataFile(Object):
    """
    This is the main API that uses a Pandas dataframe as the medium for data   
    """
    def __init__(IO):
    
        self._IO_handler = IO
        self._dataframe = self._IO_handler.load()
        
    def add_row(self, row):
        self._dataframe.loc[len(self._dataframe)] = row
        
    def remove_row(self, index)
        self._dataframe = self._dataframe.drop(index)
        
    def get():
        return self._dataframe.copy()
        
    def close():
        self._IO_handler.save()
    