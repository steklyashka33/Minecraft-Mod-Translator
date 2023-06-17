from .yaml_file_manager import YAMLFileManager
from os.path import isfile, join
import os

class UserConfigManager():
    """manager for working with the user_config file."""

    USER_CONFIG_TEMPLATE = {
        'interface_language': 'English', 
        'dict_interface_language': None, #example:  English: en.yaml
        'appearance_mode': 'System', #number from the list system_list_of_appearance_modes
        'last_path_to_mods': os.path.expanduser('~\\AppData\\Roaming\\.minecraft\\mods'),
        'last_path_to_save': os.path.expanduser('~\\Documents\\translations'),
        'startwith': '(Auto)',
        }

    FILE_NAME = "user_config.yaml"

    def __init__(self, main_folder: str) -> None:

        #checking for correct input
        self._checking_the_path(main_folder)
        self.main_folder = main_folder
    
    @staticmethod
    def _checking_the_path(folder) -> None:
        """checking the folder path for errors."""

        if isinstance(folder, str):
            if not os.path.isdir(folder):
                raise NotADirectoryError(f"Directory '{folder}' does not exist.")
        else:
            raise TypeError("Directory must be a string.")
    
    def get_user_config(self, folder_with_translations: str):
        """returns data from the user_config file."""

        #checking for correct input
        self._checking_the_path(os.path.join(self.main_folder, folder_with_translations))

        file_manager = YAMLFileManager(self.main_folder, self.FILE_NAME)
        if isfile( join(self.main_folder, self.FILE_NAME) ):
            self.user_config = file_manager.load_file()
        else:
            self.user_config = self.USER_CONFIG_TEMPLATE
        
        self.user_config['dict_interface_language'] = self._get_dictionary_of_interface_language(folder_with_translations)
        
        return self.user_config
    
    def save_user_config(self, data) -> None:
        """writes data to the user_config file."""

        file_manager = YAMLFileManager(self.main_folder, self.FILE_NAME)
        file_manager.write_to_file(data)
    
    def _get_dictionary_of_interface_language(self, folder_with_translations):
        """return dict_interface_language."""
        
        path_to_folder_with_translations = os.path.join(self.main_folder, folder_with_translations)
        manager = YAMLFileManager(path_to_folder_with_translations)

        translations_files = manager.get_yaml_files()
        dict_interface_language = {}

        for file_name in translations_files:
            manager.set_file_name(file_name)
            file_data = manager.load_file()
            
            try:
                language_name = file_data['language_name']
                dict_interface_language[language_name] = file_name
            except:
                pass
            
        return dict_interface_language



if __name__ == "__main__":
    main_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manager = UserConfigManager(main_folder)
    folder_with_translations = YAMLFileManager(main_folder, "config.yaml").load_file()["folder_with_translations"]
    data = manager.get_user_config(folder_with_translations)
    print(data)