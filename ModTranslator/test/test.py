import os
import sys
from shutil import copyfile
from json import loads

# import ModTranslator
main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, main_dir)
from mod_translator import ModTranslator

def test():

    # Получаем путь к текущей директории
    current_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(current_dir, "supported_languages_Minecraft.json"), 'r', encoding="utf8") as f:
        SUPPORT_LANGUAGES_MINECRAFT = loads(f.read())

    test_file = "test_file.jar"
    verification_file = "check.jar"
    path_test_file = os.path.join(current_dir, test_file)
    path_verification_file = os.path.join(current_dir, verification_file)

    #Проверка на наличие тестового файла.
    if os.path.isfile( path_test_file ):

        #Копировать и переименовать тестовый файл. 
        copyfile(path_test_file, path_verification_file)

        file = [verification_file]

        #Запуск программы.
        ModTranslator(SUPPORT_LANGUAGES_MINECRAFT).translate("ru", current_dir, file, command=lambda _: print(f"clone {test_file} has been translated."))

        #Deleting verification files.
        if os.path.isfile(path_verification_file):
            os.remove(path_verification_file)
            print(f"clone {test_file} deleted.")

if __name__ == '__main__':
    test()