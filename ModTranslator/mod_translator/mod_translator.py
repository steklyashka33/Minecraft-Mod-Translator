__author__ = 'Steklyashka'

from typing import Optional, Tuple, Union, Callable
from json import loads
import os
from .translator import Translator
from .zip_file_manager import ZipFileManager
from .path_to_languages import PathToLanguages
from .check_mods_translation import CheckModsTranslation

class ModTranslator:
    def __init__(self,
                 supported_languages: Union[dict, None],
                 exception_handler: Union[Callable[[Exception, str], None], None] = None):
        self._supported_languages = supported_languages
        self._exception_handler = exception_handler

    def translate(self,
                 target_language: str,
                 directory: str,
                 mod_files: list[str] = None,
                 directory_of_saves: Union[str, None] = None,
                 command: Union[Callable[[dict], None], None] = None):
        """
        target_language - язык на который нужно перевести,
        directory - директория с модами,
        mod_files - список переводимых модов с расширением jar,
        command - функция, которая получает промежуточный результат.
        """

        FROM_LANGUAGE = "en_us.json"
        target_language_code = self._supported_languages[target_language]
        self._directory = directory
        self._directory_of_saves = CheckModsTranslation._checking_the_path(directory_of_saves) if directory_of_saves else self._directory
        self._command = command

        for file_name in CheckModsTranslation(target_language_code,
                                              self._directory,
                                              mod_files,
                                              self._exception_handler).get_list_of_untranslated_mods():

            #Получение абсолютного пути мода.
            file_path = os.path.join(self._directory, file_name)

            #Получаем путь и переводы из мода.
            for path in PathToLanguages(file_path).getFolders():

                from_file = os.path.join(path, FROM_LANGUAGE).replace("\\", "/")
                to_file = os.path.join(path, target_language_code).replace("\\", "/")
                
                file_contents: dict = loads(ZipFileManager.read_file_in_ZipFile(file_path, from_file))

                #Получение перевода.
                translation = Translator().translate( list(file_contents.values()), target_language ).text

                #Подстановка переводов к ключам.
                i = dict( zip( file_contents.keys(), translation ) )

                #Сохранение.
                self._save(file_path, to_file, str(i))
                
                if self._command:
                    self._command(file_name)
    
    def _save(self, zip_file: str, file: str, string: str):
        """Saving changes."""

        comment = "//This translation was made by the ModTranslator program.\n//repository — https://github.com/steklyashka33/mod-translator-for-minecraft"
        ZipFileManager.adding_a_file( zip_file, file, comment + string )