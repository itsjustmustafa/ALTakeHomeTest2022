"""
This is a class for a CLI controller for a DataFile program. This is the C in MVC.
This is responsible for creating a user interface to allow management of data
using the DataFile API. 
"""
from dataFile import DataFile

class FileAlreadyExists(Exception):
    """
    Exception for when trying to add a file to a collection when it exists in the collection.
    """
    pass

class DataFileCLIController:
    
    def __init__(self):
        self._datafiles = []
        self._currentDataFile = None
    
    def get_datafile_names(self):
        return [datafile.get_filename() for datafile in self._datafiles]
    
    def select_datafile(self, index):
        self._currentDataFile = self._datafiles[index]
        
    
    def addFile(self, filename):
        """
        Adds a DataFile with data sourced from csv file `filename` to the Controller.
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
        dataFile = self._datafiles.pop(dataFileIndex)
        if save:
            dataFile.save()
    
    