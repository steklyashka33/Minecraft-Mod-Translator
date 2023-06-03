__author__ = 'Steklyashka'

import zipfile

class FileManager:
    
    @staticmethod
    def getFilesOfTheType(files: str, file_type: str):
        """Возращает файлы нужного расширения."""

        files_of_the_type = filter(lambda f: f.endswith(file_type),  files)

        return files_of_the_type
    
    @staticmethod
    def getFilePath(directory: str, name_file: str):
        """Возращает путь к файлу."""
        return directory + name_file



class ZipFileManager:
    """Менеджер для работы с zip-файлами."""

    @staticmethod
    def read_ZipFile(jarFile) -> list[str]:
        """Возращает содержимое файла."""
        
        with zipfile.ZipFile(jarFile, 'r') as z:
            return z.namelist()
    
    @staticmethod
    def read_file_in_ZipFile(zip_file: str, file: str) -> str:
        """
        Получает zip файл и файл в нём лежащий.
        Возращает содержимое этого файла.
        """
        with zipfile.ZipFile(zip_file, "r", allowZip64=False) as z,  \
            z.open(file, "r") as f:

            return f.read().decode('utf-8')
    
    @staticmethod
    def adding_a_file(zip_file: str, file: str, string: str):
        """Добавляет файл в zip файл. """
        #print(zip_file, file)
        with zipfile.ZipFile(zip_file, "a", allowZip64=False) as z,  \
            z.open(file, "w") as f:

            f.write( string.encode('utf-8') )




if __name__ == '__main__':

    from os.path import dirname, abspath
    main_dir = dirname(abspath(__file__))
    
    for i, j in JarManager(main_dir+r'/test.jar').getAll():
        print(i,j)
    
    from time import sleep
    sleep(100)
