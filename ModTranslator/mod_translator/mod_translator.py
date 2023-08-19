__author__ = 'Steklyashka'

from typing import List, Optional, Tuple, Union, Callable
from json import loads
from shutil import copyfile
import os, logging
from .translator import Translator
from .zip_file_manager import ZipFileManager
from .path_to_languages import PathToLanguages
from .check_mods_translation import CheckModsTranslation

class ModTranslator:
    def __init__(self,
                 comment: str = "The translation is done automatically.",
                 supported_languages: Union[dict, None] = None):
        self.COMMENT = f"//{comment}\n"
        SUPPORT_LANGUAGES = self._load_supported_languages()
        self._supported_languages = supported_languages if supported_languages else SUPPORT_LANGUAGES
        
        self.FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
        self._logger = self._create_logger(self.FORMATTER)
    
    def _load_supported_languages(self):
        # Получаем путь к текущей директории
        main_dir = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(main_dir, "supported_languages.json"), 'r', encoding="utf8") as f:
            SUPPORT_LANGUAGES = loads(f.read())
        
        return SUPPORT_LANGUAGES

    def translate(self,
                 target_language: str,
                 directory: str,
                 mod_files: Union[List[str], None] = None,
                 directory_of_saves: Union[str, None] = None,
                 startwith: str = "(Auto)"):
        """
        target_language - язык на который нужно перевести,
        directory - директория с модами,
        mod_files - список переводимых модов с расширением jar,
        """

        FROM_LANGUAGE = "en_us.json"
        target_language_code: str = self._supported_languages[target_language]
        if not target_language_code.endswith(".json"):
            target_language_code += ".json"
        self._directory = directory
        self._mod_files = self._adding_extension_to_files(mod_files, ".jar") if mod_files else None
        self._directory_of_saves = CheckModsTranslation._check_the_path(directory_of_saves) if directory_of_saves else self._directory
        self._startwith = startwith
        
        check_mods = CheckModsTranslation(target_language_code,
                                          self._directory,
                                          self._mod_files,
                                          self._exception_handler)
        untranslated_mods = check_mods.get_untranslated_mods()

        for mod_name in untranslated_mods:
            #Получение абсолютного пути мода.
            file_path = os.path.join(self._directory, mod_name)

            #Получаем путь и переводы из мода.
            for path in PathToLanguages(file_path).getFolders():
                # set the paths to the working files
                from_file = os.path.join(path, FROM_LANGUAGE).replace("\\", "/")
                to_file = os.path.join(path, target_language_code).replace("\\", "/")
                
                file_contents: dict = loads(ZipFileManager.read_file_in_ZipFile(file_path, from_file))
                texts = list(file_contents.values())
                
                try:
                    # get translation
                    translation = Translator().translate( texts, target_language )
                except TypeError: # texts has elements not of type str
                    self._logger.warning(f"unable to translate {mod_name} due to broken structure.")
                    continue

                # Подстановка переводов к ключам.
                result = dict( zip( file_contents.keys(), translation ) )

                # save
                self._save(mod_name, to_file, str(result))
    
    def get_logger(self):
        return self._logger
    
    def _exception_handler(self, comment: str):
        self._logger.warning(f"{comment}")
    
    @staticmethod
    def _adding_extension_to_files(file_names: List[str], desired_extension):
        fun = lambda file: file if file.endswith(desired_extension) else file+desired_extension
        mods = list(map(fun, file_names))
        return mods
    
    @staticmethod
    def _create_logger(formatter: logging.Formatter) -> logging.Logger:
        """creates and returns a logger."""
        
        file = os.path.basename(__file__)  # Получаем название файла
        file_name = os.path.splitext(file)[0]  # Извлекаем имя файла без расширения
    
        # create logger
        logger = logging.getLogger(file_name)
        logger.setLevel(logging.DEBUG)

        # Создание обработчика для записи логов в файл
        file_dir = os.path.dirname(__file__)
        file_handler = logging.FileHandler(f"{file_dir}\\{file_name}.log", mode='w', encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        # Добавление обработчика в логгер
        logger.addHandler(file_handler)

        return logger
    
    def _save(self, zip_mod_name: str, file_name: str, string: str):
        """Saving changes."""

        zip_file = os.path.join(self._directory_of_saves, zip_mod_name)

        if not self._directory_of_saves is self._directory:
            from_file_path = os.path.join(self._directory, zip_mod_name)
            to_file_path = os.path.join(self._directory_of_saves, zip_mod_name)
            copyfile(from_file_path, to_file_path)

        ZipFileManager.adding_a_file( zip_file, file_name, self.COMMENT + string )
        self._logger.info(f"mod {zip_mod_name} has been saved")