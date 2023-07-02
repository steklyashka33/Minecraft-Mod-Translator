from typing import Optional, Tuple, Union, Callable
from tkinter import NORMAL, BooleanVar
from .flipped_ctkcheckbox import FlippedCTkCheckBox

class CreateSwitches:
    def __init__(self,
                 master: any,
                 names: list,
                 start: int = 0,
                 state: str = NORMAL,
                 value: bool = True,
                 max_length: int = 30):
        
        indexes = range(len(names))
        self._switches = []
        self._master = master
        _state = state

        for index, name in zip(indexes, names):
            _name = name if len(name) <= max_length else name[:max_length] + "..."
            _value = BooleanVar(value=int(value))
            checkbox = FlippedCTkCheckBox(master=master, text=f"{_name}",  state=_state, variable=_value)
            checkbox.grid(row=(start + index), column=0, padx=10, pady=(0, 10), sticky="ew")
            self._switches.append(checkbox)
    
    def get(self) -> list:
        return self._switches
    
    def hide(self, switches: Union[list, None] = None) -> None:
        if switches is None:
            _switches = self._switches
        
        for i in _switches:
            i.grid_remove()

    def show(self) -> None:
        for i in self._switches:
            i.grid()