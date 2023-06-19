__author__ = 'Steklyashka'

#Изменение рабочей директории
from typing import Optional, Tuple, Union, Callable
import os
from .translator import Translator
from .path_to_languages import PathToLanguages
from .tool import ZipFileManager

class ModTranslator:
    def __init__(self, supported_languages: dict = None):
        self.supported_languages = supported_languages

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
        self._mod_files = mod_files if mod_files else os.listdir(directory)

        if not directory_of_saves or not isinstance(directory_of_saves, str):
            self._directory_of_saves = self._mod_files

        Mods = self.filter_files_by_extension(self._mod_files, ".jar")

        for file_name in list( Mods ):

            #Получение абсолютного пути мода.
            file = os.path.join(directory, file_name)

            if not os.path.isfile(file):
                raise ValueError(f"no file found {file}")

            #Вывести файлы с папкой с переводами.
            #if PathToLanguages(file).isFolderWithTranslations(): print(file)

            #Получаем путь и переводы из мода.
            for path in PathToLanguages(file).getFolders():

                if not PathToLanguages(file).isNecessaryTranslation( target_language ):

                    from_file = os.path.join(path, FROM_LANGUAGE)
                    to_file = os.path.join(path, target_language)
                    #print(from_file, to_file)

                    from json import loads

                    file_contents: dict = loads(ZipFileManager.read_file_in_ZipFile(file, from_file))

                    #Получение перевода.
                    translation = Translator().translate(  list(file_contents.values()), 'ru'  ).text

                    #Подстановка переводов к ключам.
                    i = dict( zip( file_contents.keys(), translation ) )

                    #Сохранение.
                    self._save(file, to_file, str(i))

                    file_name = os.path.basename(file)
                    
                    if command:
                        command(file_name)
    
    def filter_files_by_extension(self, file_names, desired_extension):
        filtered_files = list(filter(lambda file: file.endswith(desired_extension), file_names))
        return filtered_files
    
    def _save(self, zip_file: str, file: str, string: str):
        """Сохранение изменений."""
        comment = "//This translation was made by the ModTranslator program.\n"
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