"""
An implementation of DataFileIO for saving and loading CSV files.
"""

from dataFileIO import DataFileIO
from os.path import exists, splitext
import pandas as pd

class InvalidFileType(Exception):
    """
    Exception for when trying to select a file that is not a supported filetype.
    """
    pass


class DataFileIOCSV(DataFileIO):

    def __init__(self, filename):
        super().__init__()
        self._filename = filename
        
    def load(self):
        """
        Returns a Pandas DataFrame from the csv file `self.filename`
        :return: (optional) Pandas DataFrame if `self.filename` exists, otherwise None
        """
        if not exists(self._filename):
            raise FileNotFoundError("Could not find {}".format(self._filename))
            
        if splitext(self._filename)[1] != ".csv":
            raise InvalidFileType("Input file {} is not a csv.".format(self._filename))
            
        
        return pd.read_csv(self._filename).astype(str)

    def save(self, dataframe):
        """
        Saves a Pandas Dataframe to the csv file `self.filename`
        :param dataframe: a Pandas Dataframe
        """
        dataframe.to_csv(self._filename, index=False)