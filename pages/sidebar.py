from typing import Optional, Tuple, Union, Callable
from customtkinter import *
from utils import *
from CTkMessagebox import CTkMessagebox

class Sidebar(CTkFrame):
    def __init__(self,
                 master: any,
                 data: GetData,
                 update_language_callback: Callable[[str], None],
                 update_appearance_mode_callback: Callable[[str], None],
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[Union[int, str]] = None,
                 border_width: Optional[Union[int, str]] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 overwrite_preferred_drawing_method: Union[str, None] = None,
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self.update_language_callback = update_language_callback
        self.update_appearance_mode_callback = update_appearance_mode_callback

        self.config, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.logo_label = CTkLabel(self, text=self.config.title, font=CTkFont(size=21, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        font_label=CTkFont(size=15)

        values = list(self.user_config.dict_interface_language.keys())
        self.interface_language_label = CTkLabel(self, text=self.lang.interface_language, anchor="w", font=font_label)
        self.interface_language_label.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.interface_language_menu = CTkOptionMenu(self, values=values, command=self.update_language_callback)
        self.interface_language_menu.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.interface_language_menu.set(self.lang.language_name)

        system_list_of_appearance_modes = self.config.system_list_of_appearance_modes
        lang_list_of_appearance_modes = self.lang.list_of_appearance_modes
        self.dict_of_appearance_modes = dict(zip(lang_list_of_appearance_modes, system_list_of_appearance_modes))
        dict_of_system_appearance_modes = dict(zip(system_list_of_appearance_modes, lang_list_of_appearance_modes))
        self.appearance_mode_label = CTkLabel(self, text=self.lang.appearance_mode, anchor="w", font=font_label)
        self.appearance_mode_label.grid(row=4, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = CTkOptionMenu(self, values=self.lang.list_of_appearance_modes, command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=5, column=0, padx=10, pady=(10, 10), sticky="ew")
        self.appearance_mode_optionemenu.set(dict_of_system_appearance_modes[ self.user_config.appearance_mode ])

    def change_appearance_mode_event(self, new_appearance_mode: str):
        system_new_appearance_modes = self.dict_of_appearance_modes[new_appearance_mode]
        self.update_appearance_mode_callback(system_new_appearance_modes)
