from typing import Optional, Tuple, Union, Callable
from customtkinter import *
from utils import *
from .flipped_ctkcheckbox import FlippedCTkCheckBox
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
        self.hide_inactive_files = IntVar(value=self._session.hide_inactive_file)
        hide_inactive_files_font = CTkFont("Arial", size=16, weight="bold")
        hide_inactive_files_checkbox = CTkCheckBox(self, text=self.lang.hide_inactive_files, font=hide_inactive_files_font, variable=self.hide_inactive_files)
        hide_inactive_files_checkbox.grid(row=1, column=0)

        # create scrollable frame
        self.scrollable_frame = CTkScrollableFrame(self, label_text=self.lang.file_selection)
        self.scrollable_frame.grid(row=2, column=0, sticky="ns")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame._parent_frame.configure(width=scrollable_frame_width)
        self.scrollable_frame._parent_frame.grid_propagate(False)
        self.scrollable_frame_switches = []
        for i in range(100):
            value = IntVar(value=1)
            checkbox = FlippedCTkCheckBox(master=self.scrollable_frame, text=f"CTkCheckBox {i}", variable=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(0, 10), sticky="ew")
            self.scrollable_frame_switches.append(checkbox)
        
        # 
        self.save_untranslated_files = IntVar(value=self._session.save_untranslated_files)
        save_untranslated_files_font = CTkFont("Arial", size=14)
        save_untranslated_files_checkbox = CTkCheckBox(self, text=self.lang.save_untranslated_files, font=save_untranslated_files_font, variable=self.save_untranslated_files)
        save_untranslated_files_checkbox.grid(row=3, column=0)
        
        # 
        self.create_subfolder = IntVar(value=self._session.create_subfolder)
        save_untranslated_files_font = CTkFont("Arial", size=14)
        create_subfolder_checkbox = CTkCheckBox(self, text=self.lang.create_subfolder, font=save_untranslated_files_font, variable=self.save_untranslated_files)
        create_subfolder_checkbox.grid(row=4, column=0)
        
        # создание кнопки для продолжения
        button_font = CTkFont("Arial", size=22, weight="bold")
        next_button = CTkButton(self, width=widget_width, height=widget_height, font=button_font, text=self.lang.next, command=self.next_step)
        next_button.grid(row=5, column=0, sticky="")
    
    def next_step(self):
        pass
    
    def get_session_data(self) -> SessionData:
        """returns session data."""
        return

        hide_inactive_files = self.hide_inactive_files.get()
        save_untranslated_files = self.save_untranslated_files.get()

        session.set(hide_inactive_files=hide_inactive_files, save_untranslated_files=save_untranslated_files)

        return session