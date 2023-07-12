from typing import Optional, Tuple, Union, Callable
from pathlib import Path
from customtkinter import *
from threading import Thread
from utils import *
from ModsTranslator import *
from .create_switches import CreateSwitches
from .session_data import SessionData

class Page2(CTkFrame):
    def __init__(self,
                 master: any,
                 data: GetData,
                 session: SessionData,
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
        self.grid_rowconfigure(0, weight=4, uniform="fred")
        self.grid_rowconfigure((1, 3, 4), weight=3, uniform="fred")
        self.grid_rowconfigure(2, weight=16, uniform="fred")
        self.grid_rowconfigure(5, weight=5, uniform="fred")

        self._session = session
        self._command = command

        _, self.user_config, self.lang, self.supported_languages = data.get()
        self.main_folder = data.get_main_folder()
        
        scrollable_frame_width = 300
        widget_width = 210
        widget_height = 36

        # 
        header_font = CTkFont("Arial", size=30, weight="bold")
        main_label = CTkLabel(self, text=self.lang.file_management, font=header_font)
        main_label.grid(row=0, column=0, sticky="s")

        # 
        self.inactive_files_state = BooleanVar(value=self._session.inactive_files_state)
        inactive_files_state_font = CTkFont("Arial", size=16, weight="bold")
        inactive_files_state_checkbox = CTkSwitch(self, text=self.lang.inactive_files_state, font=inactive_files_state_font, command=self._inactive_files_event, variable=self.inactive_files_state)
        inactive_files_state_checkbox.grid(row=1, column=0)

        # create scrollable frame
        scrollable_frame = CTkScrollableFrame(self, label_text=self.lang.file_selection)
        scrollable_frame.grid(row=2, column=0, sticky="ns")
        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame._parent_frame.configure(width=scrollable_frame_width)
        scrollable_frame._parent_frame.grid_propagate(False)
        #build switches
        self.disabled_switches = None
        self.thread = Thread(target=self._build_switches_for_scrollable_frame, args=(scrollable_frame,))
        self.thread.start()

        # 
        self.save_untranslated_files = BooleanVar(value=self._session.save_untranslated_files)
        save_untranslated_files_font = CTkFont("Arial", size=14)
        save_untranslated_files_checkbox = CTkSwitch(self, text=self.lang.save_untranslated_files, font=save_untranslated_files_font, variable=self.save_untranslated_files)
        save_untranslated_files_checkbox.grid(row=3, column=0)
        
        # 
        self.create_subfolder = BooleanVar(value=self._session.create_subfolder)
        create_subfolder_font = CTkFont("Arial", size=14)
        create_subfolder_checkbox = CTkSwitch(self, text=self.lang.create_subfolder, font=create_subfolder_font, variable=self.create_subfolder)
        create_subfolder_checkbox.grid(row=4, column=0)
        
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang.next, command=self.next_step)
        next_button.grid(row=5, column=0, sticky="")

    def _inactive_files_event(self) -> None:
        if self.disabled_switches is None:
            return
        
        if self.inactive_files_state.get():
            self.disabled_switches.hide()
        else:
            self.disabled_switches.show()
        
    def _build_switches_for_scrollable_frame(self, master):
        """create switches for scrollable frame."""

        if self._session.normal_switches is None and self._session.disabled_switches is None:
            #get mods
            mods_translation = CheckModsTranslation(self.supported_languages[self._session.to_language]["mc_code"],
                                                self._session.path_to_mods,
                                                exception_handler=self._exception_handler)
            untranslated_mods = mods_translation.get_untranslated_mods()
            untranslated_names_of_mods = [Path(mod).stem for mod in untranslated_mods]
            other_mods = mods_translation.get_translated_mods() + mods_translation.get_mods_with_no_languages()
            other_names_of_mods = [Path(mod).stem for mod in other_mods]
            #get values
            normal_switches_values = True
        else:
            #get mods
            untranslated_names_of_mods = [name for name, value in self._session.normal_switches]
            other_names_of_mods = [name for name, value in self._session.disabled_switches]
            #get values
            normal_switches_values = [value for name, value in self._session.normal_switches]

        #create switches
        max_length = 30
        self.normal_switches = CreateSwitches(master, untranslated_names_of_mods, start=0, values=normal_switches_values, max_length=max_length)
        self.disabled_switches = CreateSwitches(master, other_names_of_mods, start=len(self.normal_switches.get_switches()), state=DISABLED, values=False, max_length=max_length)
        
        #hide disabled switches
        self._inactive_files_event()
    
    def next_step(self):
        if self.thread.is_alive():
            print("wait")
            return
        
        variable_switches = self.normal_switches.get_variable_switches()
        mods_for_translation = [text for text, variable in variable_switches if variable]

        session = self.get_session_data()
        session.set(mods_for_translation=mods_for_translation)

        if self._command:
            self._command(session)
    
    def get_session_data(self) -> SessionData:
        """returns session data."""
        if self.thread.is_alive():
            # self.thread.join()
            pass
        else:
            normal_switches_data = self.normal_switches.get_variable_switches()
            disabled_switches_data = self.disabled_switches.get_variable_switches()
            self._session.set(normal_switches=normal_switches_data,
                              disabled_switches=disabled_switches_data)

        #get values
        inactive_files_state = self.inactive_files_state.get()
        save_untranslated_files = self.save_untranslated_files.get()
        create_subfolder = self.create_subfolder.get()

        self._session.set(inactive_files_state=inactive_files_state, 
                          save_untranslated_files=save_untranslated_files,
                          create_subfolder=create_subfolder)

        return self._session
    
    def _exception_handler(self, file_name):
        print(f"error {file_name}")