"""
This is a class for a CLI controller for a DataFile program. This is the C in MVC.
This is responsible for creating a user interface to allow management of data
using the DataFile API. 
"""
from dataFile import DataFile
import os.path
import data_display_collector as display_collector
import pandas as pd

class FileAlreadyExists(Exception):
    """
    Exception for when trying to add a file to a collection when it exists in the collection.
    """
    pass


def _remove_start_of_path(path, start):
    """
    Removes `start` from the start of `path`
    
    :param path: The full path from which to remove the start
    :param start: The start of `path` to remove
    :type path: string
    :type start: string
    :return: `path` but with `start` removed form the start
    :rtype: string
    """
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
        """
        Get the total number of datafiles loaded in the Controller
        
        :return: total number of datafiles
        :rtype: int
        """
        return len(self._datafiles)
    
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
        """
        Set the index to the selected datafile to be queried
        
        :param index: index of the selected datafile
        :type index: int
        """
        self._current_datafile_index = index
    
    def add_row_to_current_datafile(self, row):
        """
        Adds row `row` to the currently selected DataFile.
        
        :param row: Either a list of values or a dict representing the key/values for the new row
        :type row: dict or list
        """
        self._datafiles[self._current_datafile_index].add_row(row)
    
    def remove_row_from_current_datafile(self, index):
        """
        Removes row at `index` from the currently selected DataFile.
        
        :param index: The index of the row for removal
        :type index: int
        """
        self._datafiles[self._current_datafile_index].remove_row(index)
    
    def change_row_of_current_datafile(self, row_index, selected_column, value):
        """
        Assigns the value at row `row_index` in column `column` to `value`
        
        :param row: The index of the row to be changed
        :param selected_column: The key of the column for the change
        :param value: The new value of the position in the datafile
        :type row: int
        :type selected_column: string
        :type value: string
        """
        
        
        
        old_row = self.get_current_datafile_dataframe().loc[[row_index]].to_dict('list')
        
        new_row = {}
        for column in self.get_current_datafile_columns():
            if column == selected_column:
                new_row[column] = value
            else:
                new_row[column] = old_row[column][0]
        
        self._datafiles[self._current_datafile_index].change_row(new_row, row_index)
    
    def get_current_datafile_columns(self):
        """
        Return the column names of the current DataFile's DataFrame
        
        :return: List of column names
        :rtype: list of strings
        """
        return list(self._datafiles[self._current_datafile_index].get().columns)
    
    def get_current_datafile_name(self, truncate=False):
        """
        Gets the filename of the source of the current DataFile
        
        :return: DataFile filename
        :rtype: string
        """
        datafile_names = self.get_datafile_names(truncate)  
        return datafile_names[self._current_datafile_index]
    
    def get_current_datafile_dataframe(self):
        """
        Get the current DataFile's DataFrame.
        
        :return: the current DataFile's DataFrame
        :rtype: Pandas DataFrame
        """
        return self._datafiles[self._current_datafile_index].get()
    
    def get_current_datafile_dataframe_row_total(self):
        """
        Get the total number of rows in the current DataFile
        
        :return: number of rows in DataFile
        :rtype: int
        """
        return len(self._datafiles[self._current_datafile_index])
    
    def is_current_datafile_empty(self):
        """
        Check for if the current DataFile has no rows
        
        :return: Flag whether current DataFile has no rows
        :rtype: boolean
        """
        return self.get_current_datafile_dataframe_row_total() <= 0
    
    def print_current_datafile(self, head=None):
        """
        Prints the summarized ASCII table representation of the current DataFile's DataFrame.
        Optionally prints first `head` rows (defaults to all rows)
        """
        
        
        dataframe_to_print = self.get_current_datafile_dataframe()
        
        if head != None:
            dataframe_to_print = dataframe_to_print.head(head)
        
        if len(dataframe_to_print) == 0:
            empty_df = {}
            for column in list(dataframe_to_print.columns):
                empty_df[column] = ["-"]
            print(pd.DataFrame(empty_df).to_string(index=False))
            return
        
        dataframe_to_print.index += 1
        
        print(dataframe_to_print)
    
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
    
    def get_displays_names(self):
        """
        Return the script names of all the display-method scripts
        
        :return: List if script names
        :rtype: list of strings
        """
        display_methods = display_collector.get_displays()
        return [display_methods[i].__name__.split(".")[-1] for i in range(len(display_methods))]
        
    def get_display(self, index):
        """
        Return the display function from the display list given the index of the display
        
        :param index: index of the script of the desired display method, as ordered in `get_displays_names()`
        :type index: int
        :return: List if script names
        :rtype: function
        """
        return display_collector.get_displays()[index].display     
        
    def get_queried_of_current_datafile(self, queries, reindex = False):
        """
        Gets the Pandas DataFrame after searching the current DataFile with `queries`
        
        :param queries: List of search arguments (each elememnt is [term, key, exact])
        :param reindex: (default=False) Flag to reindex the rows from 1 to total number of rows
        :type queries: List (each element is [string, string, boolean])
        :type reindex: boolean
        :return: The queried DataFrame
        :rtype: Pandas DataFrame
        """
        
        queried_df = self._datafiles[self._current_datafile_index].search_multi(queries)

        if reindex and len(queried_df) > 0:
            queried_df = queried_df.set_index(pd.Index(list(range(len(queried_df)))))
        
        return queried_df