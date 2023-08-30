from typing import Any, Optional, Tuple, Union, Callable
from threading import Timer
from customtkinter import *
from utils import *

class Page1(CTkFrame):
    def __init__(self,
                 master: Any,
                 data: GetData,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 session: Union[SessionData, None] = None,
                 command: Union[Callable[[SessionData], None], None] = None,
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self._command = command

        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure((1, 2, 3, 4), weight=6, uniform="fred") # type: ignore
        self.grid_rowconfigure(5, weight=8, uniform="fred")
        self.grid_rowconfigure((6, 7, 8), weight=6, uniform="fred") # type: ignore
        self.grid_rowconfigure((0, 9), weight=10, uniform="fred") # type: ignore

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()

        # 
        header_font = CTkFont("Arial", size=38, weight="bold")
        self.main_label = CTkLabel(self, text=self.lang.data_entry, font=header_font) # type: ignore
        self.main_label.grid(row=0, column=0, sticky="s")

        combobox_font = CTkFont("Arial", size=14)
        label_font = CTkFont("Arial", size=18)
        widget_width = 210
        widget_height = 36

        # создание подписи к вводу пути к папке с модами
        path_to_mods_font = CTkFont("Arial", size=14)
        entry_path_to_mods_label = CTkLabel(self, text=self.lang.path_to_mods, font=path_to_mods_font) # type: ignore
        entry_path_to_mods_label.grid(row=1, column=0, sticky="s")
        # создание CTkComboBox для ввода пути к папке с модами
        self.path_to_mods = StringVar()
        self.path_to_mods_entry = FolderDialogComboBox(self, width=widget_width, height=widget_height, font=combobox_font, variable=self.path_to_mods)
        self.path_to_mods_entry.grid(row=2, column=0)
        self.path_to_mods_entry.set(self.user_config.last_path_to_mods) # type: ignore

        # создание подписи для выбора языков
        language_label = CTkLabel(self, text=self.lang.translation_language, font=label_font) # type: ignore
        language_label.grid(row=3, column=0, sticky="s")
        # создание виджета CTkOptionMenu для выбора языков
        self.target_language = StringVar()
        language_font = CTkFont("Arial", size=18)
        self.language_optionmenu = CTkOptionMenu(self, width=widget_width, height=widget_height, font=language_font, variable=self.target_language)
        self.language_optionmenu.grid(row=4, column=0)
        self.language_optionmenu.set(self.lang.select_language) # type: ignore
        list_supported_languages = self.supported_languages.keys()
        CTkScrollableDropdown(self.language_optionmenu, height = 200, values=list_supported_languages, frame_corner_radius=20)

        # функция для ограничения длины строки
        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:6])
        
        # рамка для приставки к переводам
        startwith_frame = CTkFrame(self, width=widget_width, height=int(widget_height*1.33), fg_color="transparent")
        startwith_frame.grid(row=5, column=0)
        startwith_frame.grid_propagate(False)
        startwith_frame.grid_rowconfigure(0, weight=1)
        startwith_frame.grid_columnconfigure((0, 1), weight=1) # type: ignore
        # создание подписи для приставки к переводам
        startwith_font_label = CTkFont("Arial", 16)
        startwith_label = CTkLabel(startwith_frame, text=self.lang.startwith, font=startwith_font_label, anchor='w') # type: ignore
        startwith_label.grid(row=0, column=0, sticky="sew")
        # создание виджета CTkEntry для приставки к переводам
        self.startwith = StringVar(value=self.user_config.startwith) # type: ignore
        self.startwith.trace_add("write", lambda *args: character_limit(self.startwith))
        startwith_entry_font = CTkFont("Arial", size=18, weight="bold")
        startwith_width: int = (widget_width//2.5) # type: ignore
        self.startwith_entry = CTkEntry(startwith_frame, width=startwith_width, height=widget_height, font=startwith_entry_font, textvariable=self.startwith, justify='center')
        self.startwith_entry.grid(row=0, column=1, sticky="se")

        # создание подписи к вводу пути к папке созранений
        path_to_save_font = CTkFont("Arial", size=14)
        path_to_save_label = CTkLabel(self, text=self.lang.last_path_to_save, font=path_to_save_font) # type: ignore
        path_to_save_label.grid(row=6, column=0, sticky="s")
        # создание CTkComboBox для ввода пути к папке созранений
        self.path_to_save = StringVar()
        self.path_to_save_entry = FolderDialogComboBox(self, width=widget_width, height=widget_height, font=combobox_font, variable=self.path_to_save)
        self.path_to_save_entry.grid(row=7, column=0)
        self.path_to_save_entry.set(self.user_config.last_path_to_save) # type: ignore
        
        # создание надписи о невозможности продолжить
        self.error_label = CTkLabel(self, text_color="red", text=self.lang.error, font=("Arial", 14)) # type: ignore
        self.timer = None
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang.next, command=self.next_step) # type: ignore
        next_button.grid(row=9, column=0, sticky="n")

        # set session data.
        if session:
            self._set_session_data(session)
        
    def next_step(self):
        # функция, которая будет вызываться при нажатии на кнопку "Продолжить"

        #
        if self.timer:
            self.timer.cancel()

        #
        if self.target_language.get() == self.lang.select_language or not self.checking_the_path(self.path_to_mods.get()): # type: ignore
            self.error_label.grid(row=8, column=0, sticky="s")
            self.timer = Timer(5, self._error_label_timer)
            self.timer.start()
            return
        
        session = self.get_session_data()

        self.user_config.last_path_to_mods = session.path_to_mods # type: ignore
        self.user_config.last_path_to_save = session.path_to_save # type: ignore
        self.user_config.startwith = session.startwith # type: ignore
        UserConfigManager(self.main_folder).save_user_config(vars(self.user_config))

        if self._command:
            self._command(session)

    def checking_the_path(self, folder):
        try:
            UserConfigManager._checking_the_path(folder)
            return True
        except NotADirectoryError:
            return False
    
    def get_session_data(self) -> SessionData:
        """returns session data."""

        path_to_mods = self.path_to_mods.get()
        path_to_save = self.path_to_save.get()
        to_language = lang if (lang := self.target_language.get()) != self.lang.select_language else None # type: ignore
        startwith = self.startwith.get()

        session = SessionData(path_to_mods, path_to_save, to_language, startwith)

        return session
    
    def _set_session_data(self, session: SessionData) -> None:
        """set session data."""

        self.path_to_mods.set(session.path_to_mods)
        self.path_to_save.set(session.path_to_save)
        self.target_language.set(lang if (lang := session.to_language) else self.lang.select_language) # type: ignore
        self.startwith.set(session.startwith)
    
    def _error_label_timer(self) -> None:
        """Removes error_label."""

        self.error_label.grid_forget()