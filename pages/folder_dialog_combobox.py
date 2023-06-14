import tkinter
from typing import Optional, Tuple, Union, Callable
from customtkinter import *

class FolderDialogComboBox(CTkComboBox):
    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 font: Optional[Union[tuple, CTkFont]] = None,
                 state: str = tkinter.NORMAL,
                 hover: bool = True,
                 variable: Union[tkinter.Variable, None] = None,
                 command: Union[Callable[[str], None], None] = None,
                 justify: str = "left",
                 **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, 
                         bg_color, fg_color, border_color, button_color, button_hover_color, 
                         text_color = text_color, 
                         text_color_disabled = text_color_disabled, 
                         font = font, 
                         state = state, 
                         hover = hover, 
                         variable = variable, 
                         command = command, 
                         justify = justify, **kwargs)
    
    def _open_dropdown_menu(self):
        self._choose_folder()

    def _choose_folder(self):
        """function for calling the folder selection dialog."""
        
        folder_path = filedialog.askdirectory()
        if folder_path:
            self._dropdown_callback(folder_path)