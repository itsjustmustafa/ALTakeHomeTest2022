"""
The abstract class DataFileIO responsible for handling data sources of DataFiles.
Can save and load dataframes for DataFiles.
"""

class DataFileIO:
    """
    The file-handling class
    """
    def __init__(self):
        self.filename = None
    
    def save(self, dataframe):
        """
        Should save a Pandas Dataframe to a relevant location based on the DataFileIO object.
        Since this is an abstract class, there is no implementation.
        :param dataframe: The Pandas DataFrame to save
        :type dataframe: Pandas DataFrame
        """
        raise NotImplementedError("Abstract class `DataFileIO` has no save() implementation")
    
    def load(self, filename=None):
        """
        Should load the dataframe from a relevant location based on the DataFileIO object.
        Since this is an abstract class, there is no implementation.
        """
        raise NotImplementedError("Abstract class `DataFileIO` has no load(filename) implementation")
    
    def get_filename(self):
        raise NotImplementedError("Abstract class `DataFileIO` has no get_filename() implementation")