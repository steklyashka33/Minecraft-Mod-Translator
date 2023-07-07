from typing import Optional, Tuple, Union, Callable
from tkinter import NORMAL, BooleanVar
from threading import Thread, currentThread
from .flipped_ctkcheckbox import FlippedCTkCheckBox

class CreateSwitches:
    def __init__(self,
                 master: any,
                 texts: list[str],
                 start: int = 0,
                 state: str = NORMAL,
                 values: Union[bool, list[bool]] = True,
                 max_length: int = 30):
                 
        from time import time
        self.start = time()
        
        indexes = range(len(texts))
        self._switches: list[FlippedCTkCheckBox] = []
        self._variable_switches: list[tuple[str, BooleanVar]] = []
        self._master = master
        self._start = start
        self._state = state
        self._max_length = max_length

        self._threads: list[Thread] = []

        if isinstance(values, bool):
            value = values
            for index, text in zip(indexes, texts):
                self._create_thread(index, text, value)
        elif isinstance(values, list) and all(isinstance(value, bool) for value in values):
            for index, text, value in zip(indexes, texts, values):
                self._create_thread(index, text, value)
        else:
            raise TypeError("The 'values' argument should be either a Boolean value (bool) or a list of Boolean values (list[bool]), \
                            and its length should match the length of the 'texts' list.")
        
        for thread in self._threads:
            thread.join()
        
        print("the work is completed in", time()-self.start)
    
    def _create_thread(self, index, text, value):
            thread = Thread(target=self._build_switch, args=(index, text, value))
            thread.start()
            self._threads.append(thread)

    def _build_switch(self, index, text, value):
            try:
                _text = text if len(text) <= self._max_length else text[:self._max_length] + "..."
                _value = BooleanVar(value=value)
                checkbox = FlippedCTkCheckBox(master=self._master, text=f"{_text}",  state=self._state, variable=_value)
                checkbox.grid(row=(self._start + index), column=0, padx=10, pady=(0, 10), sticky="ew")
                self._switches.append(checkbox)
                self._variable_switches.append((text, _value,))
            except Exception as e:
                # print(e)
                pass

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