# dataFile module

The DataFile API, responsible for manipulating and querying DataFrames within DataFiles.
This is the M in MVC.
This uses a Pandas DataFrames as the DataFrame implementation.


### _class_ dataFile.DataFile(IO_handler)
Bases: `object`


#### \__init__(IO_handler)
Create a DataFile object.


* **Parameters**

    **IO_handler** ([*DataFileIO*](dataFileIO.md#dataFileIO.DataFileIO)) – The file handler that takes care of saving and loading



#### add_row(row)
Adds row row to _dataframe.


* **Parameters**

    **row** (*dict** or **list*) – Either a list of values or a dict representing the key/values for the new row



#### change_row(row, index)
Changes the row at position index to row


* **Parameters**

    
    * **row** (*list** or **dict*) – The replacement row to be placed at index


    * **index** (*int*) – The index of the row to be changed



#### _static_ from_csv(filename)
Returns a DataFile using a csv file as a source.
Creates a DataFileIOCSV as an IO_handler for the DataFile.    
(based on Pandas’ from_csv method)


* **Parameters**

    **filename** (*string*) – The filename for the csv data



* **Returns**

    DataFile with datasource as the csv file filename



* **Return type**

    DataFile



#### get()
Get a deep copy of _dataframe.


* **Returns**

    A deep copy of the current dataframe



* **Return type**

    Pandas DataFrame



#### get_filename()
Get filename of DataFile from _IO_handler


* **Returns**

    filename



* **Return type**

    string



#### remove_row(index, reset_index=True)
Remove a row (or a multiple rows) at a given index (or indices) from _dataframe.


* **Parameters**

    
    * **index** (*int** or **list of ints*) – either a single index, or a list of indices


    * **reset_index** (*boolean*) – (default = True), will reset the index after the rows are removed



#### save()
Save _dataframe to its source


#### search(term, key, exact=True, search_df=None)
Searches each row of _dataframe for term in the column key.
Exact search if exact, otherwise substring search.


* **Parameters**

    
    * **term** (*string*) – The string to search for in the _dataframe


    * **key** (*string*) – The column in _dataframe in which to search for term


    * **exact** (*boolean*) – (default True) If True, only return rows where values in key are exactly term, if False, return rows where term is a substring of values in key


    * **search_df** (*None** or **Pandas DataFrame*) – (defalt None) The dataframe to search within, if None, defaults to self._dataframe



* **Returns**

    DataFrame with rows from _dataframe with only rows where key value is exactly term



* **Return type**

    Pandas DataFrame



#### search_multi(search_args, current_result=None)
Executes multiple search queries on the dataframe using recursion.


* **Parameters**

    
    * **search_args** (*List** (**each element is** [**string**, **string**, **boolean**]**)*) – List of search arguments (each elememnt is [term, key, exact])


    * **current_result** (*None** or **Pandas DataFrame*) – (default=None) The current search result to continue searching, if None then defaults to _dataframe



* **Returns**

    Final result of the multiple searches



* **Return type**

    Pandas DataFrame
