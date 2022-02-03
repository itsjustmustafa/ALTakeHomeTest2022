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
        raise NotImplementedError(
            "Abstract class `DataFileIO` has no save() implementation"
        )

    def load(self, filename=None):
        """
        Should load the dataframe from a relevant location based on the DataFileIO object.
        Since this is an abstract class, there is no implementation.

        :param filename: The filename of the file to load
        :type filename: string
        """
        raise NotImplementedError(
            "Abstract class `DataFileIO` has no load(filename) implementation"
        )

    def get_filename(self):
        """
        Gets the filename of the DataFileIO

        :return: filename
        :rtype: string
        """
        return self._filename

    def __str__(self):
        """
        Should return whatever self.get_filename() returns

        :return: `self.get_filename()`
        :rtype: string
        """
        return self.get_filename()
