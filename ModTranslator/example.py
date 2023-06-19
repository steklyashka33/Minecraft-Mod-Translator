import os
from shutil import copyfile
from mod_translator import ModTranslator

def main():
    directory = os.path.abspath(input("Path to the mods folder: "))
    save_directory = os.path.abspath(input("Path to the save folder: "))

    #Проверка на наличие тестового файла.
    if os.path.isfile(current_dir + test_file):

        #Копировать и переименовать тестовый файл. 
        copyfile(current_dir + test_file, current_dir + verification_file)

        file = [verification_file]

        #Запуск программы.
        ModTranslator().translate("ru", current_dir, command=lambda file: print(f"{file} has been translated."))
        print(f"clone {test_file} deleted.")

        #Deleting verification files.
        if os.path.isfile(current_dir + verification_file):
            os.remove(current_dir + verification_file)

if __name__ == '__main__':
    main()