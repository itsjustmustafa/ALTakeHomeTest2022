from dataFileCLIController import DataFileCLIController, FileAlreadyExists
from dataFileIOCSV import InvalidFileType
import pandas as pd

pd.set_option("display.width", None)
import re
from tkinter.filedialog import askopenfilename


class DataFileCLIView:
    def __init__(self, name):
        self._name = name
        self._controller = DataFileCLIController()
        self._current_scene = "Start"
        self._running = False
        self._current_query = []
        self._is_searching = False

        self._scene_to_funct = {
            "Start": self.start_scene,
            "Exit": self.exit_scene,
            "Selection": self.selection_scene,
            "Add File": self.add_file_scene,
            "Remove File": self.remove_file_scene,
            "Querying": self.query_scene,
            "Search": self.search_scene,
            "Add Row": self.add_row_scene,
            "Remove Row Querying": self.remove_row_querying_scene,
            "Remove Row Search": self.remove_row_search_scene,
            "Change Row Querying": self.change_row_querying_scene,
            "Change Row Search": self.change_row_search_scene,
            "Display Querying": self.display_querying_scene,
            "Display Search": self.display_search_scene,
        }

    def run(self):
        """
        Begin the application
        """
        self._running = True

        while self._running:
            self._scene_to_funct[self._current_scene]()

    def _send_message(
        self, message, is_prompt=False, user_input_string="\nContinue (Enter)..."
    ):
        """
        Sends the user `message`

        :param message: message to send the user
        :param is_prompt: (default=False) Whether this message is a prompt (requires the user press enter afterwards)
        :param user_input_string: (has default) The string after the message if this is a prompt
        :type message: string
        :type is_prompt: boolean
        :type user_input_string: string
        """
        if is_prompt:
            input(message + user_input_string)
        else:
            print(message)

    def _ask_user(self, message):
        """
        Asks the user `message` and returns their response

        :param message: message to ask the user
        :type message: string
        """
        return input(message)

    def _prompt_y_n(self, message=None):
        """
        Asks the user a yes/no question, returns a boolean corresponding to their answer.
        Keeps asking until the user reponds with a valid answer ("y", "yes", "n", or "no")

        :param message: (Optional) Message to prompt the user
        :type message: (Optional) string
        :return: True if a positive response, False if a negative response
        :rtype: boolean
        """

        if message == None:
            message = "(y/n): "

        valid_choice = False
        response = None
        while not valid_choice:
            user_response = self._ask_user(message)

            if user_response.lower() in ["y", "yes"]:
                response = True
                valid_choice = True
            elif user_response.lower() in ["n", "no"]:
                response = False
                valid_choice = True
        return response

    def _prompt_choice(
        self,
        choices,
        prompt_msg=None,
        choice_msg=None,
        show_choices=True,
        allow_exit=True,
    ):
        """
        Asks the user to choose from a variety of choices by choosing the index of the desired choice.

        :param choices: list choices
        :param prompt_msg: (Optional) Prompt to ask prior to user input
        :param choice_msg: (Optional) Message prior to displaying choices
        :param show_choices: (default=True) Flag to show the list of choices
        :param allow_exit: (default=True) Flag to allow no choice
        :type choices: list of strings
        :type prompt_msg: (Optional) string
        :type choice_msg: (Optional) string
        :type show_choices: boolean
        :type allow_exit: boolean
        :return: index of choice from `choices`, -1 if no choice
        :rtype: int
        """
        if len(choices) == 0:
            raise Exception("No choices given")

        if prompt_msg == None:
            prompt_msg = 'Enter your choice (from 1 to {}) or "n" to cancel: '.format(
                len(choices)
            )

        if choice_msg == None:
            choice_msg = "Choose among the following:"

        if show_choices:
            list_msg = "\n".join(
                ["{:<10}{}".format(i + 1, choices[i]) for i in range(len(choices))]
            )
            self._send_message(choice_msg + "\n" + list_msg)
        else:
            self._send_message(choice_msg)

        valid_choice = False
        user_choice = -1
        while not valid_choice:
            user_response = self._ask_user(prompt_msg)
            if user_response == "n" and allow_exit:
                return -1
            if user_response.isnumeric():
                if int(user_response) > 0 and int(user_response) <= len(choices):
                    valid_choice = True
                    user_choice = int(user_response) - 1
                else:
                    self._send_message(
                        "Please choose between 1 and {}".format(len(choices))
                    )
            else:
                self._send_message("Please enter a number".format(len(choices)))
        return user_choice

    def _datafile_list_to_string(self):
        """
        A string representation of all the filenames of the DataFiles in `_controller`

        :return: All the filenames formatted as a table
        :rtype: string
        """
        datafile_str = "\n[ Empty ]"
        if self._controller.get_total_datafiles() > 0:
            current_datafile_names = self._controller.get_datafile_names(truncate=True)
            datafile_list_dataframe = pd.DataFrame({"Filename": current_datafile_names})
            datafile_list_dataframe.index += 1
            datafile_str = str(datafile_list_dataframe)

        return datafile_str

    def start_scene(self):
        """
        Scene for starting the applicaton.
        Scene key: Start
        """

        self._send_message("Welcome to {}.".format(self._name), True)
        self._current_scene = "Selection"

    def exit_scene(self):
        """
        Scene for exiting the applicaton.
        Asks for confirmation as well as option to save each opened DataFile
        Scene key: Exit
        """

        confirm_exit = self._prompt_y_n("Are you sure you want to exit? (y/n): ")

        if not confirm_exit:
            self._current_scene = "Selection"
            return

        datafile_filenames = self._controller.get_datafile_names(truncate=True)
        datafiles_to_save = []
        for datafile_index in range(len(datafile_filenames)):
            is_saving_this_datafile = self._prompt_y_n(
                "Unsaved DataFile:\n\t{}\nSave? (y/n): ".format(
                    datafile_filenames[datafile_index]
                )
            )
            if is_saving_this_datafile:
                datafiles_to_save.append(datafile_index)

        for datafile_index in range(len(datafile_filenames) - 1, -1, -1):
            is_saving_this_datafile = False
            if datafile_index in datafiles_to_save:
                is_saving_this_datafile = True
            self._controller.closeFile(datafile_index, save=is_saving_this_datafile)

        self._send_message("Exiting {}".format(self._name))
        self._running = False

    def selection_scene(self):
        """
        Scene for selecting an open DataFile.
        Scene key: Selection
        """
        self._send_message("\n-- DATAFILE SELECTION --\n")

        file_command_messages = {
            "select": ["Select File", "select <index>", r"select \d+\Z"],
            "add": ["Add .csv file", "add", r"add\Z"],
            "remove": ["Remove File", "remove", r"remove\Z"],
            "exit": ["Exit App", "exit", r"exit\Z"],
        }

        file_commands = ["select", "remove", "add", "exit"]

        if self._controller.get_total_datafiles() == 0:
            file_commands = ["add", "exit"]

        self._send_message(
            "-Current DataFiles-\n" + self._datafile_list_to_string() + "\n"
        )

        selected_command, user_response = self._select_command(
            file_command_messages, file_commands
        )

        match selected_command:
            case "exit":
                self._current_scene = "Exit"
                return
            case "add":
                self._current_scene = "Add File"
                return
            case "remove":
                self._current_scene = "Remove File"
                return
            case "select":

                selected_datafile_number = int(user_response.split()[1])

                if selected_datafile_number in range(
                    1, self._controller.get_total_datafiles() + 1
                ):
                    selected_datafile_index = selected_datafile_number - 1
                    self._send_message(
                        "Selected: {}".format(
                            self._controller.get_datafile_names(truncate=True)[
                                selected_datafile_index
                            ]
                        )
                    )
                    self._controller.select_datafile(selected_datafile_index)
                    self._current_scene = "Querying"
                else:
                    self._send_message(
                        "Index {} is invalid (must be between 1 and {})".format(
                            selected_datafile_number,
                            self._controller.get_total_datafiles(),
                        ),
                        True,
                    )
                pass
            case _:
                pass

    def add_file_scene(self):
        """
        Scene for adding a new DataFile.
        Scene key: Add File
        """
        self._send_message("\n-- ADDING FILE --\n")

        filename = askopenfilename(
            title="Please a CSV to add.", filetypes=[("CSV Files", [".csv"])]
        )

        self._current_scene = "Selection"

        if filename == "":
            self._send_message("No file was selected.", True)
            return

        try:
            self._controller.addFile(filename)
        except FileAlreadyExists:
            self._send_message("{} is already loaded.".format(filename), True)
        except FileNotFoundError:
            self._send_message("{} could not be found.".format(filename), True)
        except InvalidFileType:
            self._send_message("{} is not a csv.".format(filename), True)

    def remove_file_scene(self):
        """
        Scene for removing a DataFile.
        Scene key: Remove File
        """

        self._send_message("\n-- REMOVING FILE --\n")

        remove_index = self._prompt_choice(
            self._controller.get_datafile_names(truncate=True),
            choice_msg="Choose which DataFile to remove from the current workspace:",
        )

        if remove_index < 0:
            self._send_message("Removal cancelled")
            self._current_scene = "Selection"
            return

        nominated_datafile = self._controller.get_datafile_names()[remove_index]

        self._send_message("Nominated file:\n\t{}".format(nominated_datafile))
        user_confirm = self._prompt_y_n("Are you sure? (y/n): ")
        if user_confirm:
            save_confirm = self._prompt_y_n("Would you like to save this? (y/n): ")
            self._controller.closeFile(remove_index, save_confirm)
            if save_confirm:
                self._send_message("{}\n\t saved and closed".format(nominated_datafile))
            else:
                self._send_message("{}\n\t closed".format(nominated_datafile))
        else:
            self._send_message("Removal cancelled")

        self._current_scene = "Selection"

    def query_scene(self):
        """
        Scene for the query menu of the current selected DataFile.
        Scene key: Querying
        """
        self._send_message("\n-- QUERYING DATAFILE --\n")

        query_command_messages = {
            "add": ["Add a row", "add", r"add\Z"],
            "remove": ["Remove a row", "remove", r"remove\Z"],
            "change": ["Change a row", "change", r"change\Z"],
            "display": ["Display Data", "display", r"display\Z"],
            "search": ["Search Data", "search", r"search\Z"],
            "back": ["Back to DataFile selection", "back", r"back\Z"],
        }

        total_rows = self._controller.get_current_datafile_dataframe_row_total()
        self._send_message(
            self._controller.get_current_datafile_name(True)
            + " ({} row{})".format(total_rows, "" if total_rows == 1 else "s")
        )
        self._controller.print_current_datafile(head=10)

        selected_command, user_response = self._select_command(query_command_messages)

        match selected_command:
            case "add":
                self._current_scene = "Add Row"
            case "remove":
                self._current_scene = "Remove Row Querying"
            case "change":
                self._current_scene = "Change Row Querying"
            case "display":
                self._current_scene = "Display Querying"
            case "search":
                print("to search")
                self._current_scene = "Search"
            case "back":
                self._current_scene = "Selection"
            case _:
                pass

    def add_row_scene(self):
        """
        Scene for adding a new row to the current selected DataFile.
        Should return back to the Querying scene afterwards.
        Scene key: Add Row
        """

        self._send_message("\n-- ADDING ROW --\n")

        column_names = self._controller.get_current_datafile_columns()

        initial_confirm = self._prompt_y_n("Add a new row? (y/n): ")

        if initial_confirm:

            new_row = {}
            for column_name in column_names:
                new_row[column_name] = self._ask_user(
                    "Enter - {}: ".format(column_name)
                )

            cool_new_row = pd.DataFrame(pd.Series(new_row))

            self._send_message("\n-New Row-\n" + str(cool_new_row) + "\n")

            second_confirm = self._prompt_y_n("Confirm new row? (y/n): ")
            if second_confirm:
                self._controller.add_row_to_current_datafile(new_row)
                self._send_message("New row added!")
            else:
                self._send_message("Row addition cancelled")

        self._current_scene = "Querying"

    def remove_row_querying_scene(self):
        """
        Remove a row, given an index of the users choice, out of the entire currently selected DataFile
        Scene key: Remove Row Querying
        """
        self._remove_row(False)

        self._current_scene = "Querying"

    def remove_row_search_scene(self):
        """
        Remove a row, given an index of the users choice, from the queried search results
        Scene key: Remove Row Search
        """
        self._remove_row(True)

        self._current_scene = "Search"

    def _prompt_row(self, searching=False):
        """
        Prompts the user to select a row of the DataFile's DataFrame

        :param searching: (default=False) Flag if using from Search scene
        :return: list [index of row, row of DataFrame]
        :rtype: list[int, Pandas DataFrame]
        """

        index_of_interest = -1

        total_rows = len(self._controller.get_current_datafile_dataframe())
        if searching:
            total_rows = len(
                self._controller.get_queried_of_current_datafile(self._current_query)
            )
        if total_rows == 0:
            if searching:
                self._send_message("Current DataFile search is empty.", True)
            else:
                self._send_message("Current DataFile is empty.", True)
            return

        index_value_selected = self._prompt_choice(
            range(total_rows),
            choice_msg="Which row are you choosing?",
            show_choices=False,
        )

        if searching:
            dataframe_queried = self._controller.get_queried_of_current_datafile(
                self._current_query
            )
            index_of_interest = list(dataframe_queried.index)[index_value_selected]
        else:
            index_of_interest = index_value_selected

        if index_of_interest < 0:
            self._send_message("No row selected.", True)
            return

        row_of_interest = self._controller.get_current_datafile_dataframe().loc[
            [index_of_interest]
        ]

        row_of_interest = row_of_interest.set_index(pd.Index([index_of_interest + 1]))

        return [index_of_interest, row_of_interest]

    def _remove_row(self, searching=False):
        """
        Remove a row, given an index of the users choice, from the currently selected DataFile

        :param searching: (default=False) Flag if removing row from Search scene
        :type searching: boolean
        """

        index_to_remove, row_to_remove = self._prompt_row(searching)

        self._send_message("Row to remove:")
        self._send_message(row_to_remove)

        confirm_removal = self._prompt_y_n("Confirm removal of row? (y/n): ")
        if confirm_removal:
            self._controller.remove_row_from_current_datafile(index_to_remove)
            self._send_message("Row removed", True)
        else:
            self._send_message("Row removal cancelled", True)

    def change_row_querying_scene(self):
        """
        Change a value of a particular row in the currently selected DataFile's DataFrame
        Scene key: Change Row Querying
        """
        self._change_row(False)

        self._current_scene = "Querying"

    def change_row_search_scene(self):
        """
        Change a value of a particular row in the queried search results
        Scene key: Change Row Search
        """
        self._change_row(True)

        self._current_scene = "Search"

    def _change_row(self, searching=False):
        """
        Changes the value of a cell to that of the users choice,
        by row and column of the users choice.
        This is for both coming from the Querying and Search scene

        :param searching: (default=False) Flag if changing row in Search scene
        :type searching: boolean
        """

        index_to_change, row_to_change = self._prompt_row(searching)

        row_to_change = row_to_change.set_index(pd.Index([index_to_change + 1]))

        self._send_message("Row to change:")
        self._send_message(row_to_change)

        confirm_change_row = self._prompt_y_n("Confirm change of row? (y/n): ")
        if confirm_change_row:
            index_of_column_to_change = self._prompt_choice(
                self._controller.get_current_datafile_columns(),
                choice_msg="Which column are you changing?",
            )

            if index_of_column_to_change < 0:
                self._send_message(
                    "Column selection cancelled. Exiting row change", True
                )
                return

            column_name = self._controller.get_current_datafile_columns()[
                index_of_column_to_change
            ]

            new_value = self._ask_user("New value of {}: ".format(column_name))
            old_value = row_to_change.to_dict("list")[column_name][0]

            confirm_change_value = self._prompt_y_n(
                'Confirm "{}" -> "{}"? (y/n): '.format(old_value, new_value)
            )

            if confirm_change_value:
                self._controller.change_row_of_current_datafile(
                    index_to_change, column_name, new_value
                )
                self._send_message("Row changed", True)
            else:
                self._send_message("Row change cancelled", True)
        else:
            self._send_message("Row change cancelled", True)

    def display_querying_scene(self):
        """
        Display the currently selected DataFile's DataFrame
        Scene key: Display Querying
        """
        self._display(False)

        self._current_scene = "Querying"

    def display_search_scene(self):
        """
        Display the current queried DataFrame from the DataFile
        Scene key: Display Search
        """
        self._display(True)

        self._current_scene = "Search"

    def _display(self, searching=False):
        """
        Runs the display method of the user's choice, for both the Querying and Search scenes

        :param searching: (default=False) Flag if displaying from Search scene
        :type searching: boolean
        """
        all_displays = self._controller.get_displays_names()

        display_method_index = self._prompt_choice(
            all_displays, choice_msg="Choose from the following display methods:"
        )
        if display_method_index < 0:
            self._send_message("No display selected.", is_prompt=True)
            return

        display_method = self._controller.get_display(display_method_index)
        dataframe_to_display = self._controller.get_current_datafile_dataframe()
        if searching:
            dataframe_to_display = self._controller.get_queried_of_current_datafile(
                self._current_query, reindex=True
            )

        display_method(dataframe_to_display, self._send_message)

        self._send_message("\n", is_prompt=True)

    def search_scene(self):
        """
        Scene to navigate DataFile searching, similar to the Querying scene.
        Scene key: Search
        """
        self._send_message("\n-- SEARCHING DATAFILE --\n")

        search_commands = [
            "add-search",
            "remove-search",
            "remove-row",
            "remove-all-rows",
            "change",
            "display",
            "back",
        ]

        if self._current_query == []:
            search_commands = ["add-search", "back"]
            self._send_message("\n-No current search queries-")

        else:
            search_queries = {"Term": [], "Column": [], "Is Exact": []}
            for search_query in self._current_query:
                search_queries["Term"].append(search_query[0])
                search_queries["Column"].append(search_query[1])
                search_queries["Is Exact"].append(search_query[2])

            self._send_message("Current Search Queries:")
            search_queries_df = pd.DataFrame(search_queries)
            search_queries_df.index += 1
            self._send_message(search_queries_df.to_string())

            search_result_df = self._controller.get_queried_of_current_datafile(
                self._current_query, reindex=True
            )
            total_search_rows = len(search_result_df)
            self._send_message(
                "\nCurrent Search Results ({} row{}):".format(
                    total_search_rows, "" if total_search_rows == 1 else "s"
                )
            )

            if total_search_rows > 0:
                search_result_df = search_result_df.set_index(
                    pd.Index(list(range(total_search_rows)))
                )
                search_result_df.index += 1
                print(search_result_df)
            else:
                self._send_message("\n-Empty search result-\n")

        search_command_messages = {
            "add-search": ["Add a search term", "add-search", r"add-search\Z"],
            "remove-search": [
                "Remove a search term",
                "remove-search",
                r"remove-search\Z",
            ],
            "remove-row": ["Remove a row", "remove-row", r"remove-row\Z"],
            "remove-all-rows": [
                "Remove all rows in search",
                "remove-all-rows",
                r"remove-all-rows\Z",
            ],
            "change": ["Change a row", "change", r"change\Z"],
            "display": ["Display Data", "display", r"display\Z"],
            "back": ["Back to DataFile querying", "back", r"back\Z"],
        }

        selected_command, user_response = self._select_command(
            search_command_messages, search_commands
        )

        match selected_command:
            case "add-search":
                self._add_search_term()
            case "remove-search":
                self._remove_search_term()
            case "remove-row":
                self._current_scene = "Remove Row Search"
            case "remove-all-rows":
                self._remove_all_rows_in_search()
            case "change":
                self._current_scene = "Change Row Search"
            case "display":
                self._current_scene = "Display Search"
            case "back":
                self._current_scene = "Querying"
                self._current_query = []
            case _:
                pass

    def _add_search_term(self):
        """
        Prompts user to add a search term.
        """

        valid_term = False
        entered_term = ""
        while not valid_term:
            entered_term = self._ask_user("What string are you searching? ")
            if entered_term == "":
                self._send_message("Please enter a non-empty search term")
            else:
                valid_term = True

        index_of_column_to_change = self._prompt_choice(
            self._controller.get_current_datafile_columns(),
            choice_msg="Which column are you searching?",
            allow_exit=False,
        )

        entered_column = self._controller.get_current_datafile_columns()[
            index_of_column_to_change
        ]

        is_exact = self._prompt_y_n(
            "Exact search? (otherwise substring search) (y/n): "
        )

        self._current_query.append([entered_term, entered_column, is_exact])

        self._send_message("Added search query", True)

    def _remove_search_term(self):
        """
        Prompts user to remove a search term
        """
        if len(self._current_query) < 0:
            self._send_message("No search queries have been made", True)
            return

        remove_index = self._prompt_choice(
            self._current_query,
            choice_msg="Select a query to remove",
            show_choices=False,
        )

        if remove_index < 0:
            self._send_message("No search query selected", True)
            return

        self._current_query.pop(remove_index)
        self._send_message("Search query removed", True)

    def _remove_all_rows_in_search(self):
        """
        Remove all the rows in the queried DataFile from the Search scene
        """
        search_result_df = self._controller.get_queried_of_current_datafile(
            self._current_query
        )

        total_rows = len(search_result_df)

        if total_rows == 0:
            self._send_message("Current DataFile search is empty.", True)
            return

        confirm_change_row = self._prompt_y_n(
            "Confirm deletion of {} row{}? (y/n): ".format(
                total_rows, "" if total_rows == 1 else "s"
            )
        )

        if confirm_change_row:
            indices_to_remove = list(search_result_df.index)

            self._controller.remove_row_from_current_datafile(indices_to_remove)
            self._send_message(
                "Removed {} row{}".format(total_rows, "" if total_rows == 1 else "s"),
                True,
            )
        else:
            self._send_message(
                "Cancelled removal of {} row{}".format(
                    total_rows, "" if total_rows == 1 else "s"
                ),
                True,
            )

    def _select_command(self, command_messages, valid_commands=None):
        """
        Given a list of commands and a dictionary of command messages, prompts the user until they
        enter a valid command

        :param command_messages: dict of commands
        :param valid_commands: (Optional) list of keys for allowed commands in `command_messages`, if None assume all
        :type: command_messages: dict with values [string, string, string]
        :type valid_commands: (Optional) list of strings
        :return: list of [selected_command, user_response]
        :rtype: [string, string]
        """

        if valid_commands == None:
            valid_commands = list(command_messages)

        padding_size = max(
            20, 2 + max([len(command_messages[k][0]) for k in valid_commands])
        )
        option_message = "\n".join(
            [
                ("{:" + str(padding_size) + "}").format(command_messages[command][0])
                + "usage: {}".format(command_messages[command][1])
                for command in valid_commands
            ]
        )

        self._send_message("\nChoose one of the following commands:\n" + option_message)

        valid_response = False
        response = None
        attempted_command = None
        while not valid_response:
            response = self._ask_user(">>>")
            if len(response.split()) == 0:
                continue

            if response.split()[0] in valid_commands:
                attempted_command = response.split()[0]
                command_message = command_messages[attempted_command]
                if None == re.match(command_message[2], response):
                    self._send_message(
                        'Invalid use of {}, valid usage is "{}"'.format(
                            attempted_command, command_message[1]
                        )
                    )
                else:
                    valid_response = True
            else:
                self._send_message("Invalid response: {}".format(response))

        return attempted_command, response


if __name__ == "__main__":
    my_app = DataFileCLIView("My App")
    my_app.run()
