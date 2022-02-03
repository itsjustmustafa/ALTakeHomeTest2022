# dataFileIO module

The abstract class DataFileIO responsible for handling data sources of DataFiles.
Can save and load dataframes for DataFiles.


### _class_ dataFileIO.DataFileIO()
Bases: `object`

The file-handling class


#### \__init__()

#### get_filename()
Gets the filename of the DataFileIO


* **Returns**

    filename



* **Return type**

    string



#### load(filename=None)
Should load the dataframe from a relevant location based on the DataFileIO object.
Since this is an abstract class, there is no implementation.


* **Parameters**

    **filename** (*string*) – The filename of the file to load



#### save(dataframe)
Should save a Pandas Dataframe to a relevant location based on the DataFileIO object.
Since this is an abstract class, there is no implementation.


* **Parameters**

    **dataframe** (*Pandas DataFrame*) – The Pandas DataFrame to save
