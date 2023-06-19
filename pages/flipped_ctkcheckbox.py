import tkinter
from typing import Callable, Optional, Tuple, Union
from customtkinter import CTkCheckBox
from customtkinter.windows.widgets.font import CTkFont



class FlippedCTkCheckBox(CTkCheckBox):
    def __init__(self,
                 master: any,
                 width: int = 100,
                 height: int = 24,
                 checkbox_width: int = 24,
                 checkbox_height: int = 24,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 checkmark_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 text: str = "CTkCheckBox",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 textvariable: Union[tkinter.Variable, None] = None,
                 state: str = tkinter.NORMAL,
                 hover: bool = True,
                 command: Union[Callable[[], None], None] = None,
                 onvalue: Union[int, str] = 1,
                 offvalue: Union[int, str] = 0,
                 variable: Union[tkinter.Variable, None] = None,
                 **kwargs):
        super().__init__(master, width, height, checkbox_width, checkbox_height, corner_radius, border_width, bg_color, fg_color, hover_color, border_color, checkmark_color, text_color, text_color_disabled, text, font, textvariable, state, hover, command, onvalue, offvalue, variable, **kwargs)
        
        self._canvas.grid(row=0, column=2, sticky="e")
        self._text_label.grid(row=0, column=0, sticky="w")
        self._text_label["anchor"] = "w"