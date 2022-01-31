from dataFileIO import DataFileIO
from os.path import exists, splitext
import pandas as pd

class DataFileIOCSV(DataFileIO):

    def __init__(self, filename):
        self.filename = filename
        super().__init__()
        
    def load(self):
        """
        Returns a Pandas DataFrame from the csv file `self.filename`
        :return: (optional) Pandas DataFrame if `self.filename` exists, otherwise None
        """
        if not exists(self.filename):
            return None
            
        if splitext(self.filename)[1] != ".csv":
            return None
        
        return pd.read_csv(self.filename)
        
    def save(self, dataframe):
        """
        Saves a Pandas Dataframe to the csv file `self.filename`
        :param dataframe: a Pandas Dataframe
        """
        dataframe.to_csv(self.filename, index=False)
        