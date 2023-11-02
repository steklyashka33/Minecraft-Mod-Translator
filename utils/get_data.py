from typing import Union
from .yaml_file_manager import YAMLFileManager
from .user_config_manager import UserConfigManager
from .dataclass import DataClass
import os

class GetData:
    """work with data."""

    def __init__(self, main_folder) -> None:
        self._main_folder = main_folder
        self._user_config_manager = UserConfigManager(self._main_folder)

    def get(self) -> tuple[DataClass, DataClass, DataClass, dict]:
        """returns config, user_config, lang, supported_languages data."""
        
        # get config
        config = YAMLFileManager(self._main_folder, "config.yaml").load_file()
        
        #get user_config
        folder_with_translations = config["folder_with_translations"]
        user_config = self._user_config_manager.get_user_config(folder_with_translations)

        try:
            #get lang
            language_file = user_config["dict_interface_language"][ user_config["interface_language"] ]
        except KeyError as e:
            user_config["interface_language"] = "English"
            language_file = user_config["dict_interface_language"][ user_config["interface_language"] ]
        lang = YAMLFileManager(os.path.join( self._main_folder, folder_with_translations ), language_file).load_file()

        #get supported_languages
        supported_languages_file_name = "supported_languages.yaml"
        supported_languages = YAMLFileManager(self._main_folder, supported_languages_file_name).load_file()

        config_class = DataClass(**config)
        user_config_class = DataClass(**user_config)
        lang_class = DataClass(**lang)

        return config_class, user_config_class, lang_class, supported_languages

    def is_first_launch_of_app(self) -> Union[bool, None]:
        return self._user_config_manager.is_first_launch_of_app()

    def get_main_folder(self):
        """returns main_folder."""
        return self._main_folder