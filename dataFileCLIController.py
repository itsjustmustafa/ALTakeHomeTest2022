"""
This is a class for a CLI controller for a DataFile program. This is the C in MVC.
This is responsible for creating a user interface to allow management of data
using the DataFile API. 
"""
from dataFile import DataFile
import os.path

class FileAlreadyExists(Exception):
    """
    Exception for when trying to add a file to a collection when it exists in the collection.
    """
    pass


def _remove_start_of_path(path, start):
    path_split = os.path.abspath(path).split(os.path.sep)
    start_split = os.path.abspath(start).split(os.path.sep)
    
    if len(path_split) <= len(start_split):
        return ""
    
    if path.startswith(start):
        return os.path.join(*path_split[len(start_split):])

class DataFileCLIController:
    
    def __init__(self):
        self._datafiles = []
        self._current_datafile_index = None
    
    def get_total_datafiles(self):
        return len(self._datafiles)
    
    def print_datafile(self, index):
        print(self._datafiles[index].get())
    
    def get_datafile_names(self, truncate=False):
        """
        Get the list of DataFile filenames from `_datafiles`.
        If truncate, only return the path after the common path.
        
        :param truncate: (default=False) flag to truncate path of filenames
        :type truncate: boolean
        :return: list of filenames
        :rtype: list of strings
        """
    
        if len(self._datafiles) == 0:
            return []
    
        
    
        datafile_names = [os.path.abspath(datafile.get_filename()) for datafile in self._datafiles]
        if truncate :
            if len(self._datafiles) == 1:
                return [os.path.basename(self._datafiles[0].get_filename())]
            else:
                common_path = os.path.commonpath(datafile_names)
                return [ _remove_start_of_path(datafile_name, common_path) for datafile_name in datafile_names]
        else:
            return datafile_names
    
    def select_datafile(self, index):
        self._current_datafile_index = index
        
    def add_row_to_current_datafile(self, row):
        """
        Adds row `row` to the currently selected DataFile.
        :param row: Either a list of values or a dict representing the key/values for the new row
        :type row: dict or list
        """
        self._datafiles[self._current_datafile_index].add_row(row)
    
    def get_current_datafile_columns(self):
        """
        Return the column names of the current DataFile's DataFrame
        :return: List of column names
        :rtype: list of strings
        """
        return list(self._datafiles[self._current_datafile_index].get().columns)
    
    def get_current_datafile_name(self, truncate=False):
    
        datafile_names = self.get_datafile_names(truncate)  
        return datafile_names[self._current_datafile_index]
    
    def print_current_datafile(self):
        """
        Prints the summarized ASCII table representation of the current DataFile's DataFrame.
        """
        print(self._datafiles[self._current_datafile_index].get())
    
    def addFile(self, filename):
        """
        Adds a DataFile with data sourced from csv file `filename` to the list `_datafiles`.
        Currently only supports csv files.
        :param filename: The name of the file to add
        :type filename: string
        """
        all_filenames = [datafile.get_filename() for datafile in self._datafiles]
        
        if filename in all_filenames:
            raise FileAlreadyExists()
       
        newDataFile = DataFile.from_csv(filename)
        
        self._datafiles.append(newDataFile)
    
    def closeFile(self, dataFileIndex, save=True):
        """
        Removes a DataFile from the Controller's list, given an index, and optionally saves it.
        :param dataFileIndex: The name of the file to add
        :param save: (default=True) Flag to save the DataFile
        :type dataFileIndex: int
        :type save: boolean
        """
        dataFile = self._datafiles.pop(dataFileIndex)
        if save:
            dataFile.save()
    
    