from typing import Optional, Tuple, Union, Callable
from customtkinter import *
from utils import *
from .flipped_ctkcheckbox import FlippedCTkCheckBox
from .session_data import SessionData

class Page2(CTkFrame):
    def __init__(self,
                 master: any,
                 data: GetData,
                 session: dict,
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

        self.grid_columnconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure(0, weight=3, uniform="fred")
        self.grid_rowconfigure((1,3), weight=2, uniform="fred")
        self.grid_rowconfigure(2, weight=10, uniform="fred")
        self.grid_rowconfigure(4, weight=3, uniform="fred")

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()
        
        widget_width = 210
        widget_height = 36

        # 
        header_font = CTkFont("Arial", size=30, weight="bold")
        self.main_label = CTkLabel(self, text=self.lang.file_management, font=header_font)
        self.main_label.grid(row=0, column=0, sticky="s")

        # 
        hide_inactive_files_font = CTkFont("Arial", size=16, weight="bold")
        self.hide_inactive_files_checkbox = CTkCheckBox(self, text=self.lang.hide_inactive_files, font=hide_inactive_files_font)
        self.hide_inactive_files_checkbox.grid(row=1, column=0)

        # create scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self, label_text=self.lang.file_selection)
        self.scrollable_frame.grid(row=2, column=0, padx=50, pady=(0, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            value = IntVar(value=1)
            checkbox = FlippedCTkCheckBox(master=self.scrollable_frame, text=f"CTkCheckBox {i}", variable=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(checkbox)
        
        # 
        header_font = CTkFont("Arial", size=14, weight="bold")
        self.main_label = CTkCheckBox(self, text=self.lang.save_untranslated_files, font=header_font)
        self.main_label.grid(row=3, column=0)
        
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang.next, command=self.next_step)
        next_button.grid(row=4, column=0, sticky="")
    
    def next_step(self):
        pass
    
    def get_session_data(self) -> dict:
        """returns session data."""
        return

        path_to_mods = self.path_to_mods.get()
        path_to_save = self.path_to_save.get()
        to_language = lang if (lang := self.target_language.get()) != self.lang.select_language else None
        startwith = self.startwith.get()

        session = SessionData(path_to_mods, path_to_save, to_language, startwith)

        return session
    
    def _set_session_data(self, session) -> None:
        """set session data."""
        return

        self.path_to_mods.set(session.path_to_mods)
        self.path_to_save.set(session.path_to_save)
        self.target_language.set(lang if (lang := session.to_language) else self.lang.select_language)
        self.startwith.set(session.startwith)