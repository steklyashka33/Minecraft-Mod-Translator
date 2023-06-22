import os
from typing import Optional, Tuple, Union, Callable
from .path_to_languages import PathToLanguages
from functools import lru_cache

class CheckModsTranslation:
    @lru_cache(maxsize=3)
    def __init__(self, 
                 target_language_code: str,
                 directory: str,
                 mod_files: list[str] = None,
                 exception_handler: Union[Callable[[Exception, str], None], None] = None) -> None:
        
        if not target_language_code.endswith(".json"):
            target_language_code += ".json"
        
        self._list_of_translated_mods: list = []
        self._list_of_untranslated_mods: list = []
        self._list_of_mods_with_no_languages: list = []
        
        FROM_LANGUAGE = "en_us.json"
        self._directory = self._checking_the_path(directory)
        self._mod_files = mod_files if mod_files else os.listdir(self._directory)
        self._mod_files = self._filter_files_by_extension(self._mod_files, ".jar")
        self._exception_handler = exception_handler

        for file_name in list( self._mod_files ):

            #Получение абсолютного пути мода.
            file_path = os.path.join(self._directory, file_name)

            if not os.path.isfile(file_path):
                comment = f"no file found {file_name}"
                if self._exception_handler:
                    self._exception_handler(FileNotFoundError, comment)
                    continue
                else:
                    raise FileNotFoundError(comment)
            
            manager = PathToLanguages(file_path)

            if not manager.isFolderWithTranslations():
                self._list_of_mods_with_no_languages.append(file_name)

            elif manager.isNecessaryTranslation(target_language_code):
                self._list_of_translated_mods.append(file_name)

            else:
                self._list_of_untranslated_mods.append(file_name)
    
    def get_all(self):
        return (self._list_of_translated_mods, 
                self._list_of_untranslated_mods, 
                self._list_of_mods_with_no_languages)

    def get_list_of_translated_mods(self):
        return self._list_of_translated_mods
    
    def get_list_of_untranslated_mods(self):
        return self._list_of_untranslated_mods
    
    def get_list_of_mods_with_no_languages(self):
        return self._list_of_mods_with_no_languages

    @staticmethod
    def _filter_files_by_extension(file_names, desired_extension):
        filtered_files = list(filter(lambda file: file.endswith(desired_extension), file_names))
        return filtered_files
    
    @staticmethod
    def _checking_the_path(folder: str) -> str:
        """checking the folder path for errors."""

        if isinstance(folder, str):
            if not os.path.isdir(folder):
                raise NotADirectoryError(f"Directory '{folder}' does not exist.")
        else:
            raise TypeError("Directory must be a string.")
        return folder