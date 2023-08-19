from typing import Any, Optional, Tuple, Union, Callable
from datetime import datetime
from shutil import copyfile
from customtkinter import *
from threading import Thread
from utils import *
from ModTranslator import *
from .session_data import SessionData

class Page3(CTkFrame):
    def __init__(self,
                 master: Any,
                 data: GetData,
                 session: SessionData,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 command: Union[Callable[[SessionData], None], None] = None,
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure(0, weight=3, uniform="fred")
        self.grid_rowconfigure(1, weight=3, uniform="fred")
        self.grid_rowconfigure(2, weight=18, uniform="fred")
        self.grid_rowconfigure(3, weight=6, uniform="fred")

        self._session = session
        self._command = command

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()
        
        widget_width = 210
        widget_height = 36

        # 
        header_font = CTkFont("Arial", size=30, weight="bold")
        main_label = CTkLabel(self, text=self.lang.file_management, font=header_font) # type: ignore
        main_label.grid(row=0, column=0, sticky="")

        # создание подписи к 
        path_to_save_font = CTkFont("Arial", size=26)
        path_to_save_label = CTkLabel(self, text=self.lang.log, font=path_to_save_font) # type: ignore
        path_to_save_label.grid(row=1, column=0, sticky="s")

        # create textbox 
        textbox = CTkTextbox(self, width=350)
        textbox.grid(row=2, column=0, sticky="ns")
        textbox.configure(state=DISABLED)

        #
        from .texthandler import TextHandler
        COMMENT = "This translation was made by the Minecraft-Mods-Translator program.\n//repository — https://github.com/steklyashka33/Minecraft-Mods-Translator"
        self.translator = ModTranslator(COMMENT)
        handler = TextHandler(textbox)
        handler.setFormatter(self.translator.FORMATTER)
        self.logger = self.translator.get_logger()
        self.logger.addHandler(handler)
        self.thread = Thread(target=self._start_translating, args=())
        self.thread.start()
        
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        close_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang.close, command=self.next_step) # type: ignore
        close_button.grid(row=3, column=0, sticky="")
    
    def _start_translating(self):
        if self._session.create_subfolder:
            now = datetime.now()
            path_to_save_folder = os.path.join(self._session.path_to_save, now.strftime("%d-%m %H;%M")).replace("\\", "/") + "/"
            os.mkdir(path_to_save_folder)
        else:
            path_to_save_folder = self._session.path_to_save
        language: dict = self.supported_languages[self._session.to_language]
            
        self.translator.translate(language["google_code"],
                             self._session.path_to_mods,
                             self._session.mods_for_translation,
                             path_to_save_folder,
                             self._session.startwith)

        for mod in self._session.other_mods:
            path_to_mods = self._session.path_to_mods
            
            path_to_mod = os.path.join(path_to_mods, mod).replace("\\", "/") + ".jar"
            path_to_save = os.path.join(path_to_save_folder, mod).replace("\\", "/") + ".jar"
            copyfile(path_to_mod, path_to_save)
            self.logger.info(f"file {mod} copied to the save folder")
        
        #finish
        self.logger.info("Complete.")
    
    def next_step(self):
        if self.thread.is_alive():
            print("wait")
            return

        session = self.get_session_data()
        session.set()

        if self._command:
            self._command(session) # type: ignore
    
    def get_session_data(self) -> SessionData:
        """returns session data."""
        if self.thread.is_alive():
            # self.thread.join()
            return

        return self._session
    
    def _exception_handler(self, file_name):
        print(f"error {file_name}")