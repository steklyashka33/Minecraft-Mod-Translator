from .yaml_file_manager import YAMLFileManager
from .user_config_manager import UserConfigManager
import os

class GetData:
    def __init__(self, main_folder) -> None:
        self.main_folder = main_folder

    def get(main_folder):
        """returns config, user_config, lang, supported_languages data."""
        
        # get config
        config = YAMLFileManager(main_folder, "config.yaml").load_file()
        
        #get user_config
        folder_with_translations = config["folder_with_translations"]
        user_config = UserConfigManager(main_folder).get_user_config(folder_with_translations)

        #get lang
        language_file = user_config["dict_interface_language"][ user_config["interface_language"] ]
        lang = YAMLFileManager(os.path.join( main_folder, folder_with_translations ), language_file).load_file()

        #get supported_languages
        supported_languages_file_name = "supported_languages.yaml"
        supported_languages = YAMLFileManager(main_folder, supported_languages_file_name).load_file()

        return config, user_config, lang, supported_languages