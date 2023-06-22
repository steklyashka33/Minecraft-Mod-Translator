__author__ = 'Steklyashka'

from .zip_file_manager import ZipFileManager
import os

class PathToLanguages:
    """Получает на вход полный путь к моду(игры minecraft),
    а возращяет путь и содержание папки с переводами."""

    def __init__(self, mod_file: str) -> None:
        self._File = mod_file
        self.__folders, self.__List_of_translations = _Tools.getPathToLanguages( mod_file )
    
    def getAll(self) -> tuple[ tuple[str], tuple[ list[str] ] ]:
        """Возращает zip[path, translations]."""
        return zip(self.__folders, self.__List_of_translations)

    def getListOfTranslations(self) -> tuple[ list[str] ]:
        """Возращает переводы."""
        return self.__List_of_translations
    
    def getFolders(self) -> tuple[str]:
        """Возращает путь к переводам."""
        return self.__folders
    
    def getNameFile(self) -> str:
        """Возвращает имя файла."""
        return self._File
    
    def isFolderWithTranslations(self) -> bool:
        """Возращает True/False при существоввании или отсутствии папки с переводами."""
        return bool(self.__folders)
    
    def isNecessaryTranslation(self, lang) -> bool:
        """Возращает True/False при существоввании или отсутствии нужного перевода."""
        
        return not any([
            lang not in translations \
                for translations in self.__List_of_translations
                ])


    
class _Tools:
    """Получает на вход полный путь к jar моду(игры minecraft),
    а возращяет путь и содержание папки с переводами."""
    
    @classmethod
    def getPathToLanguages(cls, mod_file) -> tuple[   tuple[ str ], tuple[ list[str] ]   ]:
        """Возращает переводы и их директорию."""

        PATH = 'assets/' #Директория
        FROM_LANGUAGE = "en_us.json"

        #Чтение файла
        namelist = ZipFileManager.read_ZipFile(mod_file)

        #Получение содержимого директории - PATH
        namelist = cls._getArchiveSlice(PATH, namelist)

        #Получение содержимого папок lang
        func = lambda f: os.path.basename(os.path.dirname(f)) == 'lang' and os.path.basename(f)
        namelist = list( filter(func, namelist) )

        #Получение директорий файлов
        folders = cls._unique_folders(namelist)

        #Проверка на наличае FROM_LANGUAGE
        func = lambda f: os.path.join(f, FROM_LANGUAGE)
        namelist = list( filter(func, namelist) )
        
        #Получение названий файлов
        List_of_translations = [cls._getArchiveDirectory(folder, namelist.copy()) for folder in folders]

        return tuple(folders), tuple(List_of_translations)
    
    @classmethod
    def _unique_folders(cls, path_list):
        unique_folders_set = set()

        for path in path_list:
            folder = os.path.dirname(path)
            unique_folders_set.add(folder)

        return list(unique_folders_set)

    @classmethod
    def _getArchiveDirectory(cls, directory: str, archive: list) -> list:
        """Возращает содержимое директории."""
        
        archive_slice = cls._getArchiveSlice(directory, archive)

        func = lambda path_file: os.path.basename(path_file)
        archive_directory = map(func, archive_slice)

        return list(archive_directory)
    
    @staticmethod
    def _getArchiveSlice(directory: str, archive: list) -> list:
        """Возращает полный путь содержимого директории. Отсекает остальное."""
        
        def func(s: str):
            return s.startswith(directory)

        archive_slice = filter(func, archive)

        return list(archive_slice)