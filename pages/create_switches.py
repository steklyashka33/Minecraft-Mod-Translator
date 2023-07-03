from typing import Optional, Tuple, Union, Callable
from tkinter import NORMAL, BooleanVar
from threading import Thread
from .flipped_ctkcheckbox import FlippedCTkCheckBox

class CreateSwitches:
    def __init__(self,
                 master: any,
                 texts: list,
                 start: int = 0,
                 state: str = NORMAL,
                 value: bool = True,
                 max_length: int = 30):
        
        indexes = range(len(texts))
        self._switches: list[FlippedCTkCheckBox] = []
        self._variable_switches: list[tuple[str, BooleanVar]] = []
        self._master = master
        self._start = start
        self._state = state
        self._value = value
        self._max_length = max_length

        threads: list[Thread] = []
        
        for index, text in zip(indexes, texts):
            thread = Thread(target=self._build_switch, args=(index, text))
            thread.start()
            threads.append(thread)
        
        for thread in threads:
            thread.join()

    def _build_switch(self, index, text):
            _text = text if len(text) <= self._max_length else text[:self._max_length] + "..."
            _value = BooleanVar(value=self._value)
            checkbox = FlippedCTkCheckBox(master=self._master, text=f"{_text}",  state=self._state, variable=_value)
            checkbox.grid(row=(self._start + index), column=0, padx=10, pady=(0, 10), sticky="ew")
            self._switches.append(checkbox)
            self._variable_switches.append((text, _value,))

    def get_switches(self) -> list:
        """return switches."""
        return self._switches
    
    def get_variable_switches(self) -> list[tuple[str, bool]]:
        """return the list with texts and values."""
        return [(text, variable.get()) for text, variable in self._variable_switches]
    
    def hide(self, switches: Union[list, None] = None) -> None:
        if switches is None:
            _switches = self._switches
        
        for i in _switches:
            i.grid_remove()

    def show(self, switches: Union[list, None] = None) -> None:
        if switches is None:
            _switches = self._switches

        for i in _switches:
            i.grid()