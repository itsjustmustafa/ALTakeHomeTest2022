# dataFileIOCSV module

An implementation of DataFileIO for saving and loading CSV files.


### _class_ dataFileIOCSV.DataFileIOCSV(filename)
Bases: [`dataFileIO.DataFileIO`](dataFileIO.md#dataFileIO.DataFileIO)


#### \__init__(filename)

#### load()
Returns a Pandas DataFrame from the csv file self.filename


* **Returns**

    (Optional) Pandas DataFrame from filename if self.filename exists, otherwise None



* **Return type**

    (Optional) Pandas DataFrame



#### save(dataframe)
Saves a Pandas Dataframe to the csv file self.filename


* **Parameters**

    **dataframe** – a Pandas Dataframe



### _exception_ dataFileIOCSV.InvalidFileType()
Bases: `Exception`

Exception for when trying to select a file that is not a supported filetype.
