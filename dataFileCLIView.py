from dataFileCLIController import DataFileCLIController

class DataFileCLIView:
    
    def __init__(self, name):
        self._name = name
        self._controller = DataFileCLIController()
        self._currentScene = "Start"
        self._running = False
        self._current_query = None
        
        self._scene_to_funct = {
            "Start" : self.startSceneShow,
            "Exit"   : self.exitSceneShow
        }
        
    def run(self):
        self._running = True
        
        while(self._running):
            self._scene_to_funct[self._currentScene]()
    
    def _send_message(self, message, is_prompt=False):
        if is_prompt:
            input(message)
        else:
            print(message)
    
    def _ask_user(self, message):
        return input(message)
    
    def startSceneShow(self):
        self._send_message("Welcome to {}.\nPress Enter to Continue...\n".format(self._name), True)      
        self._currentScene = "Exit"
        
    def exitSceneShow(self):
        self._send_message("Exiting {}".format(self._name))
        self._running = False

    def selectionSceneShow(self):
        current_datafile_names = self._controller.get_datafile_names()
        
        datafile_names_list_message = ""
        
        file_options = {
            "select": ["Select File", "select [index]"],
            "add"   : ["Add File", "add"],
            "remove": ["Remove File", "remove [index]"]
        }
        
        if len(current_datafile_names) > 0:
            for i in range(len(current_datafile_names)):
                datafile_names_list_message += "\n{}\t{}".format(i+1, current_datafile_names[i])
        else:
            datafile_names_list_message = "\n-- Empty --"
        
        
        
        

if __name__ == "__main__":
    my_app = DataFileCLIView("My App")
    my_app.run()
    