__author__ = 'Steklyashka'

import zipfile

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
        with zipfile.ZipFile(zip_file, "r", allowZip64=False) as zf,  \
            zf.open(file, "r") as f:

            return f.read().decode('utf-8')
    
    @staticmethod
    def adding_a_file(zip_file: str, file: str, string: str):
        """Добавляет файл в zip файл. """
        
        with zipfile.ZipFile(zip_file, "a", allowZip64=False) as z,  \
            z.open(file, "w") as f:

            f.write( string.encode('utf-8') )

