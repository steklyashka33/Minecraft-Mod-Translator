from yaml_file_manager import YAMLFileManager
from os.path import isfile, join

class UserConfigManager():
    """manager for working with the user_config file."""
    def __init__(self, main_folder) -> None:
        self.FILE_NAME = "user_config.yaml"
        self.CONFIG_FILE_NAME = "config.yaml"
        self.main_folder = main_folder

        self.USER_CONFIG_TEMPLATE = {
            'interface_language': 'English', 
            'dict_interface_language': None, #example:  English: en.yaml
            'appearance_mode': 0, #number from the list system_list_of_appearance_modes
            'last_path_entry': '',
            'startwith': '(Au)',
            }
    
    def get_user_config(self):
        manager = YAMLFileManager(self.main_folder)
        if isfile( join(self.main_folder, self.FILE_NAME) ):
            pass
        else:
            self.user_config = self.USER_CONFIG_TEMPLATE
            self.user_config['dict_interface_language'] = self._get_dictionary_of_interface_language()
    
    def _get_dictionary_of_interface_language(self):
        configuration_file_data = YAMLFileManager(self.main_folder, self.CONFIG_FILE_NAME).load_file()
        folder_with_translations = configuration_file_data['folder_with_translations']
        path_to_folder_with_translations = self.main_folder + folder_with_translations
        manager = YAMLFileManager(path_to_folder_with_translations)

        translations_files = manager.get_yaml_files()
        for file in translations_files:
            manager.set_file_name(file)
            file_data = manager.load_file()
            
            try:
                language_name = file_data['language_name']
            except:
                language_name = None


if __name__ == "__main__":
    UserConfigManager(r'C:\Users\PC\Documents\GitHub\mod-translator-for-minecraft').get_user_config()