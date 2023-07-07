__author__ = 'Steklyashka'

from typing import Optional, Tuple, Union, Callable
from json import loads
from shutil import copyfile
import os
from .translator import Translator
from .zip_file_manager import ZipFileManager
from .path_to_languages import PathToLanguages
from .check_mods_translation import CheckModsTranslation

class ModTranslator:
    def __init__(self,
                 supported_languages: Union[dict, None] = None,
                 exception_handler: Union[Callable[[Exception, str], None], None] = None):
        self.SUPPORT_LANGUAGES = self._load_supported_languages()
        self._supported_languages = supported_languages if supported_languages else self.SUPPORT_LANGUAGES
        self._exception_handler = exception_handler
    
    def _load_supported_languages(self):
        # Получаем путь к текущей директории
        main_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(main_dir, "supported_languages.json"), 'r', encoding="utf8") as f:
            SUPPORT_LANGUAGES = loads(f.read())
        
        return SUPPORT_LANGUAGES

    def translate(self,
                 target_language: str,
                 directory: str,
                 mod_files: list[str] = None,
                 directory_of_saves: Union[str, None] = None,
                 command: Union[Callable[[str], None], None] = None):
        """
        target_language - язык на который нужно перевести,
        directory - директория с модами,
        mod_files - список переводимых модов с расширением jar,
        command - функция, которая получает промежуточный результат.
        """

        FROM_LANGUAGE = "en_us.json"
        target_language_code: str = self._supported_languages[target_language]
        if not target_language_code.endswith(".json"):
            target_language_code += ".json"
        self._directory = directory
        self._mod_files = self._adding_extension_to_files(mod_files, ".jar")
        self._directory_of_saves = CheckModsTranslation._checking_the_path(directory_of_saves) if directory_of_saves else self._directory
        self._command = command

        for file_name in CheckModsTranslation(target_language_code,
                                              self._directory,
                                              self._mod_files,
                                              self._exception_handler).get_untranslated_mods():

            #Получение абсолютного пути мода.
            file_path = os.path.join(self._directory, file_name)

            #Получаем путь и переводы из мода.
            for path in PathToLanguages(file_path).getFolders():

                from_file = os.path.join(path, FROM_LANGUAGE).replace("\\", "/")
                to_file = os.path.join(path, target_language_code).replace("\\", "/")
                
                file_contents: dict = loads(ZipFileManager.read_file_in_ZipFile(file_path, from_file))

                #Получение перевода.
                texts = list(file_contents.values())
                translation = Translator().translate( texts, target_language )

                if texts is translation:
                    print(f"unable to translate {file_name} due to broken structure.")

                #Подстановка переводов к ключам.
                result = dict( zip( file_contents.keys(), translation ) )

                #Сохранение.
                self._save(file_name, to_file, str(result))
                
                if self._command:
                    self._command(file_name)
    
    @staticmethod
    def _adding_extension_to_files(file_names, desired_extension):
        fun = lambda file: file if file.endswith(desired_extension) else file+desired_extension
        files = list(map(fun, file_names))
        return files
    
    def _save(self, zip_file_name: str, file: str, string: str):
        """Saving changes."""

        COMMENT = "//This translation was made by the ModTranslator program.\n//repository — https://github.com/steklyashka33/mod-translator-for-minecraft\n"
        zip_file = os.path.join(self._directory_of_saves, zip_file_name)

        if not self._directory_of_saves is self._directory:
            from_file_path = os.path.join(self._directory, zip_file_name)
            to_file_path = os.path.join(self._directory_of_saves, zip_file_name)
            copyfile(from_file_path, to_file_path)

        ZipFileManager.adding_a_file( zip_file, file, COMMENT + string )