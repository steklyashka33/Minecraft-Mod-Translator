from typing import Optional, Tuple, Union, Callable
from customtkinter import *
from utils import *
from .folder_dialog_combobox import FolderDialogComboBox


class Page1(CTkFrame):
    def __init__(self,
                 master: any,
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
                 command: Union[Callable[[dict], None], None] = None,
                 
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self._command = command

        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7), weight=6, uniform="fred")
        self.grid_rowconfigure((0), weight=10, uniform="fred")
        self.grid_rowconfigure((8), weight=8, uniform="fred")

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()

        # 
        header_font = CTkFont("Arial", size=38, weight="bold")
        self.main_label = CTkLabel(self, text=self.lang["label_data_entry"], font=header_font)
        self.main_label.grid(row=0, column=0, columnspan=3, pady=10)

        label_font = CTkFont("Arial", size=18)
        widget_font = CTkFont("Arial", size=18)
        widget_width = 210
        widget_height = 42

        # создание подписи к вводу пути к папке
        entry_label = CTkLabel(self, text=self.lang["label_enter_path"], font=label_font)
        entry_label.grid(row=1, column=0, sticky="s")
        
        # создание CTkComboBox для ввода пути к папке
        self.directory_path = StringVar()
        self.folder_entry = FolderDialogComboBox(self, width=widget_width, height=widget_height, font=CTkFont("Arial", size=14), variable=self.directory_path)
        self.folder_entry.grid(row=2, column=0)
        self.folder_entry.set(self.user_config["last_path_entry"])

        # создание подписи для выбора языков
        language_label = CTkLabel(self, text=self.lang["label_translation_language"], font=label_font)
        language_label.grid(row=3, column=0, sticky="s")
        
        # создание виджета CTkOptionMenu для выбора языков
        self.target_language = StringVar()
        language_font = CTkFont("Arial", size=20)
        self.language_optionmenu = CTkOptionMenu(self, width=widget_width, height=widget_height, font=language_font, variable=self.target_language)
        self.language_optionmenu.grid(row=4, column=0)
        self.language_optionmenu.set(self.lang["label_Select_language"])
        list_supported_languages = self.supported_languages.keys()
        CTkScrollableDropdown(self.language_optionmenu, height = 200, values=list_supported_languages, frame_corner_radius=20)

        # создание подписи для пристаке
        startwith_label = CTkLabel(self, text=self.lang["label_startwith"], font=("Arial", 14))
        startwith_label.grid(row=5, column=0, sticky="s")

        # функция для ограничения длины строки
        def character_limit(entry_text):
            if len(entry_text.get()) > 0:
                entry_text.set(entry_text.get()[:6])
        
        # создание виджета CTkEntry для приставки к переводам
        self.startwith = StringVar(value=self.user_config["startwith"])
        self.startwith.trace_add("write", lambda *args: character_limit(self.startwith))
        startwith_font = CTkFont("Arial", size=22, weight="bold")
        self.startwith_entry = CTkEntry(self, width=widget_width, height=widget_height, font=startwith_font, textvariable=self.startwith, justify='center')
        self.startwith_entry.grid(row=6, column=0)
        
        # создание надписи о невозможности продолжить
        self.error_label = CTkLabel(self, text_color="red", text=self.lang["label_error"], font=("Arial", 14))

        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang["label_next"], command=self.next_step)
        next_button.grid(row=8, column=0, sticky="n")
        
    def next_step(self):
        # функция, которая будет вызываться при нажатии на кнопку "Продолжить"

        #
        if self.target_language.get() == self.lang["label_Select_language"] or not self.checking_the_path(self.directory_path.get()):
            self.error_label.grid(row=7, column=0, sticky="s")
            return
        
        self.session = self.get_session_data()

        self.user_config["last_path_entry"] = self.session["path"]
        self.user_config["startwith"] = self.session["startwith"]
        UserConfigManager(self.main_folder).save_user_config(self.user_config)

        if self._command:
            self._command(self.session)

    def checking_the_path(folder):
        try:
            UserConfigManager._checking_the_path(folder)
            return True
        except:
            return False
    
    def get_session_data(self) -> dict:
        """returns session data."""

        path = self.directory_path.get()
        to_language = lang if (lang := self.target_language.get()) != self.lang["label_Select_language"] else None
        startwith = self.startwith.get()

        session = {
            "path": path,
            "to_language": to_language,
            "startwith": startwith,
        }
        return session
    
    def set_session_data(self, session) -> None:
        """set session data."""

        self.directory_path.set(session["path"])
        self.target_language.set(lang if (lang := session["to_language"]) else self.lang["label_Select_language"])
        self.startwith.set(session["startwith"])