__author__ = 'Steklyashka'

from typing import Optional, Tuple, Union, Callable
import os
from .translator import Translator
from .path_to_languages import PathToLanguages
from .zip_file_manager import ZipFileManager
from .check_mods_translation import CheckModsTranslation

class ModTranslator:
    def __init__(self,
                 supported_languages: Union[dict, None] = None,
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
        self._directory = self._checking_the_path(directory)
        self._mod_files = mod_files if mod_files else os.listdir(self._directory)
        self._directory_of_saves = self._checking_the_path(directory_of_saves) if directory_of_saves else self._directory
        self._command = command

        self._mod_files = self._filter_files_by_extension(self._mod_files, ".jar")

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

            #Вывести файлы с папкой с переводами.
            print(list(PathToLanguages(file_path).getAll()))

            #Получаем путь и переводы из мода.
            for path in PathToLanguages(file_path).getFolders():

                if not PathToLanguages(file_path).isNecessaryTranslation( target_language ):

                    from_file = os.path.join(path, FROM_LANGUAGE)
                    to_file = os.path.join(path, target_language)
                    #print(from_file, to_file)

                    from json import loads

                    file_contents: dict = loads(ZipFileManager.read_file_in_ZipFile(file_path, from_file))

                    #Получение перевода.
                    translation = Translator().translate(  list(file_contents.values()), 'ru'  ).text

                    #Подстановка переводов к ключам.
                    i = dict( zip( file_contents.keys(), translation ) )

                    #Сохранение.
                    self._save(file_path, to_file, str(i))
                    
                    if self._command:
                        self._command(file_name)
    
    @classmethod
    def check_mods_translation(cls,
                               target_language_code: str,
                               directory: str,
                               mod_files: list[str] = None,
                               exception_handler: Union[Callable[[Exception, str], None], None] = None) -> Union[bool, None]:
        if not target_language_code.endswith(".json"):
            target_language_code += ".json"
        
        FROM_LANGUAGE = "en_us.json"
        _directory = cls._checking_the_path(directory)
        _mod_files = mod_files if mod_files else os.listdir(_directory)
        _mod_files = cls._filter_files_by_extension(_mod_files, ".jar")
        _exception_handler = exception_handler

        for file_name in list( _mod_files ):

            #Получение абсолютного пути мода.
            file_path = os.path.join(_directory, file_name)

            if not os.path.isfile(file_path):
                comment = f"no file found {file_name}"
                if _exception_handler:
                    _exception_handler(FileNotFoundError, comment)
                    continue
                else:
                    raise FileNotFoundError(comment)

    @staticmethod
    def _filter_files_by_extension(file_names, desired_extension):
        filtered_files = list(filter(lambda file: file.endswith(desired_extension), file_names))
        return filtered_files
    
    @staticmethod
    def _checking_the_path(folder) -> None:
        """checking the folder path for errors."""

        if isinstance(folder, str):
            if not os.path.isdir(folder):
                raise NotADirectoryError(f"Directory '{folder}' does not exist.")
        else:
            raise TypeError("Directory must be a string.")
        return folder
    
    def _save(self, zip_file: str, file: str, string: str):
        """Saving changes."""

        comment = "//This translation was made by the ModTranslator program.\n//repository — https://github.com/steklyashka33/mod-translator-for-minecraft"
        ZipFileManager.adding_a_file( zip_file, file, comment + string )

'''class Scan:

    @staticmethod
    class ModsInformation:

        def __init__(self) -> None:
            pass

    @classmethod
    def Start(self, directory, lang) -> ModsInformation:
        """Возращает информацию о модах."""

        jarFiles = FileManager.getFilesOfTheType(directory, ".jar")

        for file_name in list( jarFiles ):

            jarFile = FileManager.getFilePath(directory, file_name)
'''