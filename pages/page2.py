from typing import Optional, Tuple, Union, Callable
from customtkinter import *
from utils import *

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

        l = CTkLabel(self, text="yes")
        l.pack()
    
    def get_session_data(self) -> dict:
        """returns session data."""
        return

        path_to_mods = self.path_to_mods.get()
        path_to_save = self.path_to_save.get()
        to_language = lang if (lang := self.target_language.get()) != self.lang["label_select_language"] else None
        startwith = self.startwith.get()

        session = {
            "path_to_mods": path_to_mods,
            "path_to_save": path_to_save,
            "to_language": to_language,
            "startwith": startwith,
        }
        return session
    
    def _set_session_data(self, session) -> None:
        """set session data."""
        return

        self.path_to_mods.set(session["path_to_mods"])
        self.path_to_save.set(session["path_to_save"])
        self.target_language.set(lang if (lang := session["to_language"]) else self.lang["label_select_language"])
        self.startwith.set(session["startwith"])