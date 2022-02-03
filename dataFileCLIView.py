from dataFileCLIController import DataFileCLIController, FileAlreadyExists
from dataFileIOCSV import InvalidFileType
import pandas as pd
pd.set_option('display.width', None)
import re
from tkinter.filedialog import askopenfilename

class DataFileCLIView:
    
    def __init__(self, name):
        self._name = name
        self._controller = DataFileCLIController()
        self._current_scene = "Start"
        self._running = False
        self._current_query = None
        self._is_searching = False
        
        self._scene_to_funct = {
            "Start"      : self.start_scene,
            "Exit"       : self.exit_scene,
            "Selection"  : self.selection_scene,
            "Add File"   : self.add_file_scene,
            "Remove File": self.remove_file_scene,
            "Querying"   : self.query_scene,
            "Add Row"    : self.add_row_scene,
            "Remove Row" : self.remove_row_scene,
            "Change Row" : self.change_row_scene,
            "View"       : self.view_scene,
            "Search"     : self.search_scene
        }
        
    def run(self):
        self._running = True
        
        while(self._running):
            self._scene_to_funct[self._current_scene]()
    
    def _send_message(self, message, is_prompt=False, user_input_string="\nContinue (Enter)..."):
        if is_prompt:
            input(message + user_input_string)
        else:
            print(message)
    
    def _ask_user(self, message):
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
        
    def _prompt_choice(self, choices, prompt_msg = None, choice_msg=None):
        if len(choices) == 0:
            raise Exception("No choices given")
  
        if prompt_msg == None:
            prompt_msg = "Enter your choice (from 1 to {}) or \"n\' to cancel: ".format(len(choices))
        
        if choice_msg == None:
            choice_msg = "Choose among the following:"

        list_msg = "\n".join(["{:<10}{}".format(i+1, choices[i]) for i in range(len(choices))])
        self._send_message(choice_msg + "\n" + list_msg)
        
        valid_choice = False
        user_choice = -1
        while not valid_choice:
            user_response = self._ask_user(prompt_msg)
            if user_response == "n":
                return -1
            if user_response.isnumeric():
                if int(user_response) > 0 and int(user_response) <= len(choices):
                    valid_choice = True
                    user_choice = int(user_response) - 1
                else:
                    self._send_message("Please choose between 1 and {}".format(len(choices)))
            else:
                self._send_message("Please enter a number".format(len(choices)))
        return user_choice
                    

    def _datafile_list_to_string(self):
        
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
        Scene key: Exit
        """
        self._send_message("Exiting {}".format(self._name))
        self._running = False

    def selection_scene(self):
        """
        Scene for selecting an open DataFile.
        Scene key: Selection
        """
        self._send_message("\n-- DATAFILE SELECTION --\n")
        
        file_command_messages = {
            "select": ["Select File", "select <index>", r'select \d+\Z'],
            "add"   : ["Add .csv file", "add", r'add\Z'],
            "remove": ["Remove File", "remove", r'remove\Z'],
            "exit"  : ["Exit App", "exit", r'exit\Z']
        }

        file_commands = ["select", "remove", "add", "exit"]
        
        if self._controller.get_total_datafiles() == 0:
            file_commands = ["add", "exit"]
        
        self._send_message("-Current DataFiles-\n" + self._datafile_list_to_string()+ "\n")
        
        selected_command, user_response = self._select_command(file_command_messages, file_commands)
        
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
                
                if selected_datafile_number in range(1, self._controller.get_total_datafiles() + 1):                
                    selected_datafile_index = selected_datafile_number - 1
                    self._send_message("Selected: {}".format(self._controller.get_datafile_names(truncate=True)[selected_datafile_index]))
                    self._controller.select_datafile(selected_datafile_index)
                    self._current_scene = "Querying"
                else:
                    self._send_message("Index {} is invalid (must be between 1 and {})".format(
                        selected_datafile_number, self._controller.get_total_datafiles()), True)
                pass
            case _:
                pass
            
    
    def add_file_scene(self):
        """
        Scene for adding a new DataFile.
        Scene key: Add File
        """
        self._send_message("\n-- ADDING FILE --\n")
        
        filename = askopenfilename(title='Please a CSV to add.',
                           filetypes=[('CSV Files', ['.csv'])])
        
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
        
        remove_index = self._prompt_choice(self._controller.get_datafile_names(truncate=True),
                                           choice_msg = "Choose which DataFile to remove from the current workspace:")
        
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
            "add"   : ["Add a row", "add", r'add\Z'],
            "remove": ["Remove a row", "remove <index>", r'remove \d+\Z'],
            "change": ["Change a row", "change <index>", r'change \d+\Z'],
            "view"  : ["View Data", "view", r'view\Z'],
            "back"  : ["Back to DataFile selection", "back", r'back\Z']
        }
        
        
        self._send_message(self._controller.get_current_datafile_name(True))
        self._controller.print_current_datafile()

        
        selected_command, user_response = self._select_command(query_command_messages)
        
        match selected_command:
            case "back":
                self._current_scene = "Selection"
            case "add":
                self._current_scene = "Add Row"
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
                new_row[column_name] = self._ask_user("Enter - {}: ".format(column_name))
            
            cool_new_row = pd.DataFrame(pd.Series(new_row))
            
            self._send_message("\n-New Row-\n" + str(cool_new_row) + "\n")

            valid_confirm = False
            while not valid_confirm:
                second_confirm = self._prompt_y_n("Confirm new row? (y/n): ")
                if second_confirm:
                    valid_confirm = True
                    self._controller.add_row_to_current_datafile(new_row)
                    self._send_message("New row added!")
                else:
                    valid_confirm = True
                    self._send_message("Row addition cancelled")
        
        
        self._current_scene = "Querying"
        
    def remove_row_scene(self):
        pass
        
    def change_row_scene(self):
        pass
        
    def view_scene(self):
        pass
    
    def search_scene(self):
        pass
    
    def _select_command(self, command_messages, valid_commands=None):
        """
        Given a list of commands and a dictionary of command messages, prompts the user until they
        enter a valid command
        :param command_messages: dict of commands
        :param valid_commands: (Optional) list of keys for allowed commands in `command_messages`, if None assume all are valid
        :type: command_messages: dict with values [string, string, string]
        :type valid_commands: (Optional) list of strings
        :return: list of [selected_command, user_response]
        :rtype: [string, string]
        """
        
        if valid_commands == None:
            valid_commands = list(command_messages)
        
        padding_size = max(20, 2+max([len(command_messages[k][0]) for k in valid_commands]))
        option_message = "\n".join([("{:" + str(padding_size) +"}").format(command_messages[command][0])
                                            + "usage: {}".format(command_messages[command][1])
                                            for command in valid_commands])
        
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
                        "Invalid use of {}, valid usage is \"{}\"".format(attempted_command, command_message[1]))
                else:
                    valid_response = True
            else:
                self._send_message("Invalid response: {}".format(response))
        
        return attempted_command, response
        

if __name__ == "__main__":
    my_app = DataFileCLIView("My App")
    my_app.run()
    