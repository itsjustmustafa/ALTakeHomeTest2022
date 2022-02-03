# dataFileCLIController module

This is a class for a CLI controller for a DataFile program. This is the C in MVC.
This is responsible for creating a user interface to allow management of data
using the DataFile API.


### _class_ dataFileCLIController.DataFileCLIController()
Bases: `object`


#### \__init__()

#### addFile(filename)
Adds a DataFile with data sourced from csv file filename to the list _datafiles.
Currently only supports csv files.


* **Parameters**

    **filename** (*string*) – The name of the file to add



#### add_row_to_current_datafile(row)
Adds row row to the currently selected DataFile.


* **Parameters**

    **row** (*dict** or **list*) – Either a list of values or a dict representing the key/values for the new row



#### change_row_of_current_datafile(row_index, selected_column, value)
Assigns the value at row row_index in column column to value


* **Parameters**

    
    * **row** (*int*) – The index of the row to be changed


    * **selected_column** (*string*) – The key of the column for the change


    * **value** (*string*) – The new value of the position in the datafile



#### closeFile(dataFileIndex, save=True)
Removes a DataFile from the Controller’s list, given an index, and optionally saves it.


* **Parameters**

    
    * **dataFileIndex** (*int*) – The name of the file to add


    * **save** (*boolean*) – (default=True) Flag to save the DataFile



#### get_current_datafile_columns()
Return the column names of the current DataFile’s DataFrame


* **Returns**

    List of column names



* **Return type**

    list of strings



#### get_current_datafile_dataframe()
Get the current DataFile’s DataFrame.


* **Returns**

    the current DataFile’s DataFrame



* **Return type**

    Pandas DataFrame



#### get_current_datafile_dataframe_row_total()
Get the total number of rows in the current DataFile


* **Returns**

    number of rows in DataFile



* **Return type**

    int



#### get_current_datafile_name(truncate=False)
Gets the filename of the source of the current DataFile


* **Returns**

    DataFile filename



* **Return type**

    string



#### get_datafile_names(truncate=False)
Get the list of DataFile filenames from _datafiles.
If truncate, only return the path after the common path.


* **Parameters**

    **truncate** (*boolean*) – (default=False) flag to truncate path of filenames



* **Returns**

    list of filenames



* **Return type**

    list of strings



#### get_display(index)
Return the display function from the display list given the index of the display


* **Parameters**

    **index** (*int*) – index of the script of the desired display method, as ordered in get_displays_names()



* **Returns**

    List if script names



* **Return type**

    function



#### get_displays_names()
Return the script names of all the display-method scripts


* **Returns**

    List if script names



* **Return type**

    list of strings



#### get_queried_of_current_datafile(queries, reindex=False)
Gets the Pandas DataFrame after searching the current DataFile with queries


* **Parameters**

    
    * **queries** (*List** (**each element is** [**string**, **string**, **boolean**]**)*) – List of search arguments (each elememnt is [term, key, exact])


    * **reindex** (*boolean*) – (default=False) Flag to reindex the rows from 1 to total number of rows



* **Returns**

    The queried DataFrame



* **Return type**

    Pandas DataFrame



#### get_total_datafiles()
Get the total number of datafiles loaded in the Controller


* **Returns**

    total number of datafiles



* **Return type**

    int



#### is_current_datafile_empty()
Check for if the current DataFile has no rows


* **Returns**

    Flag whether current DataFile has no rows



* **Return type**

    boolean



#### print_current_datafile(head=None)
Prints the summarized ASCII table representation of the current DataFile’s DataFrame.
Optionally prints first head rows (defaults to all rows)


#### remove_row_from_current_datafile(index)
Removes row at index from the currently selected DataFile.


* **Parameters**

    **index** (*int*) – The index of the row for removal



#### select_datafile(index)
Set the index to the selected datafile to be queried


* **Parameters**

    **index** (*int*) – index of the selected datafile



### _exception_ dataFileCLIController.FileAlreadyExists()
Bases: `Exception`

Exception for when trying to add a file to a collection when it exists in the collection.
