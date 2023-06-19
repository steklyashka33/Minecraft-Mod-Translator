__author__ = 'Steklyashka'

from .tool import *
from os.path import dirname, basename

class PathToLanguages:
    """Получает на вход полный путь к моду(игры minecraft),
    а возращяет путь и содержание папки с переводами."""

    def __init__(self, mod_file: str) -> None:
        self._File = mod_file
        self.__folders, self.__List_of_translations = _Tools.getPathToLanguages( mod_file )
    
    def getAll(self) -> list[   tuple[ str ], tuple[ list[str] ]   ]:
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
        FROM_LANGUAGE = "en_us.json"
        return not any([
            (lang not in translations and \
            FROM_LANGUAGE in translations)
                for translations in self.__List_of_translations
                ])


    
class _Tools:
    """Получает на вход полный путь к jar моду(игры minecraft),
    а возращяет путь и содержание папки с переводами."""
    
    @classmethod
    def getPathToLanguages(cls, mod_file) -> tuple[   tuple[ str ], tuple[ list[str] ]   ]:
        """Возращает переводы и их директорию."""

        PATH = 'assets/' #Директория

        #Чтение файла
        namelist = ZipFileManager.read_ZipFile(mod_file)

        #Получение содержимого директории - PATH
        namelist = cls._getArchiveSlice(PATH, namelist)

        #Получение содержимого папок lang
        func = lambda f: (s := f.split('/'))[-2] == 'lang' and s[-1]
        namelist = list( filter(func, namelist) )

        #Получение директорий файлов
        func = lambda name: dirname(name)+'/'
        folders = set(map( func, namelist ))
        
        #Получение названий файлов
        List_of_translations = [cls._getArchiveDirectory(folder, namelist.copy()) for folder in folders]

        return tuple(folders), tuple(List_of_translations)
    
    @classmethod
    def _getArchiveDirectory(cls, directory: str, archive: list) -> list:
        """Возращает содержимое директории."""
        
        archive_slice = cls._getArchiveSlice(directory, archive)

        func = lambda path_file: basename(path_file)
        archive_directory = map(func, archive_slice)

        return list(archive_directory)
    
    @staticmethod
    def _getArchiveSlice(directory: str, archive: list) -> list:
        """Возращает полный путь содержимого директории. Отсекает остальное."""
        
        def func(s: str):
            return s.startswith(directory)

        archive_slice = filter(func, archive)

        return list(archive_slice)

if __name__ == '__main__':

    from os.path import dirname, abspath
    main_dir = dirname(abspath(__file__))

    file = input('Enter the full path to the file: ') #r'C:\Users\PC\AppData\Roaming\.minecraft\versions\Create Flavored\mods\moreminecarts-1.5.4.jar'
    print([i for i in PathToLanguages(file).getAll()])