# dataFileCLIView module


### _class_ dataFileCLIView.DataFileCLIView(name)
Bases: `object`


#### \__init__(name)

#### add_file_scene()
Scene for adding a new DataFile.
Scene key: Add File


#### add_row_scene()
Scene for adding a new row to the current selected DataFile.
Should return back to the Querying scene afterwards.
Scene key: Add Row


#### change_row_querying_scene()
Change a value of a particular row in the currently selected DataFile’s DataFrame
Scene key: Change Row Querying


#### change_row_search_scene()
Change a value of a particular row in the queried search results
Scene key: Change Row Search


#### display_querying_scene()
Display the currently selected DataFile’s DataFrame
Scene key: Display Querying


#### display_search_scene()
Display the current queried DataFrame from the DataFile
Scene key: Display Search


#### exit_scene()
Scene for exiting the applicaton.
Asks for confirmation as well as option to save each opened DataFile
Scene key: Exit


#### query_scene()
Scene for the query menu of the current selected DataFile.
Scene key: Querying


#### remove_file_scene()
Scene for removing a DataFile.
Scene key: Remove File


#### remove_row_querying_scene()
Remove a row, given an index of the users choice, out of the entire currently selected DataFile
Scene key: Remove Row Querying


#### remove_row_search_scene()
Remove a row, given an index of the users choice, from the queried search results
Scene key: Remove Row Search


#### run()
Begin the application


#### search_scene()
Scene to navigate DataFile searching, similar to the Querying scene.
Scene key: Search


#### selection_scene()
Scene for selecting an open DataFile.
Scene key: Selection


#### start_scene()
Scene for starting the applicaton.
Scene key: Start
