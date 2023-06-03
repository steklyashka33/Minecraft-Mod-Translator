__author__ = 'Steklyashka'

#Изменение рабочей директории
from os.path import dirname, abspath

main_dir = dirname(abspath(__file__)) + "/"

from Input import *
from Translator import Translator
from PathToLanguages import PathToLanguages
from tool import FileManager as fManager
from tool import ZipFileManager
from os.path import isfile

class Programm:
    
    @classmethod
    def Start(cls, mod_files: list, directory: str, target_language: str, print =
               lambda file_name: print(f"{file_name} переведён")):
        """
        Запуск программы.
        mod_files - список переводимых модов с расширением jar,
        directory - директория с модами,
        target_language - язык на который нужно перевести,
        print - функция, которая выводит промежуточный результат.
        """

        FROM_LANGUAGE = "en_us.json"

        Mods = fManager.getFilesOfTheType(mod_files, ".jar")

        for file_name in list( Mods ):

            #Получение абсолютного пути мода.
            file = fManager.getFilePath(directory, file_name)

            #print(file)

            if not isfile(file):
                raise ValueError(f"no file found {file}")

            #Вывести файлы с папкой с переводами.
            #if PathToLanguages(file).isFolderWithTranslations(): print(file)

            #Получаем путь и переводы из мода.
            for path in PathToLanguages(file).getFolders():

                if not PathToLanguages(file).isNecessaryTranslation( target_language ):

                    from_file = fManager.getFilePath(path, FROM_LANGUAGE)
                    to_file = fManager.getFilePath(path, target_language)
                    #print(from_file, to_file)

                    from json import loads

                    file_contents: dict = loads(ZipFileManager.read_file_in_ZipFile(file, from_file))

                    #Получение перевода.
                    translation = Translator().translate(  list(file_contents.values()), 'ru'  ).text

                    #Подстановка переводов к ключам.
                    i = dict( zip( file_contents.keys(), translation ) )

                    #Сохранение.
                    cls.__save(file, to_file, str(i))
                    print(f"{file_name} переведён")
    


    @classmethod
    def _StandardMode(cls, path, translations):
        """Запуск программы в стандартном режиме."""

    @staticmethod
    def __save(zip_file: str, file: str, string: str):
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

        jarFiles = fManager.getFilesOfTheType(directory, ".jar")

        for file_name in list( jarFiles ):

            jarFile = fManager.getFilePath(directory, file_name)
'''


if __name__ == '__main__':
    from os import listdir
    from os import remove
    from shutil import copyfile

    files = listdir(directory)

    test_file = "test file.jar"

    verification_file = "check.jar"

    #Проверка на наличие тестового файла.
    if isfile(main_dir+ test_file ):

        #Удаление прошлой проверки.
        if isfile(main_dir+ verification_file ):
            remove(main_dir+ verification_file )

        #Копировать и переименовать тестовый файл. 
        copyfile(main_dir+ test_file, main_dir+ verification_file )

        file = [ verification_file, "234" ]

        #Запуск программы.
        Programm.Start(file, directory, target_language)