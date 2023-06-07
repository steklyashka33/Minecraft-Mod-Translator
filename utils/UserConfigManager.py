from YAMLFileManager import YAMLFileManager
from os.path import isfile, join

class UserConfigManager():
    def __init__(self, main_folder) -> None:
        self.USER_CONFIG_FILE = "user_config.yaml"
        self.CONFIG_FILE = "config.yaml"
        self.main_folder = main_folder
    
    def get_user_config(self):
        if isfile( join(self.main_folder, self.FILE_NAME) ):
            pass
        else:
            pass