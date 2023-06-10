from yaml_file_manager import YAMLFileManager
from user_config_manager import UserConfigManager

class DataFileManager(UserConfigManager):
    def __init__(self, main_folder):
        self.main_folder = main_folder
    
    def get_data(self):
        pass

if __name__ == "__main__":
    maneger = YAMLFileManager("/lang", "ru")