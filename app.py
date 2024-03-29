from customtkinter import *
from utils import *
from pages import *
from typing import Union
from CTkMessagebox import CTkMessagebox
from PIL import Image
import os


class App(CTk):
    def __init__(self):
        super().__init__()

        self.main_folder = os.path.dirname(os.path.abspath(__file__))
        self.data = GetData(self.main_folder)
        
        self.config, self.user_config, _, _ = self.data.get()

        # get supported_languages
        # print(dict( [[a["google_code"], a["mc_code"]] for a in i.values()] ))

        # создание главного окна
        self.title( self.config.title ) # type: ignore
        window_width = 640
        window_height = 480

        set_appearance_mode(self.user_config.appearance_mode)  # Modes: "System" (standard), "Dark", "Light" # type: ignore
        set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = (screen_width - window_width)//2
        y_cordinate = (screen_height - window_height)//2
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.resizable(False, False)
        self.iconbitmap(self.config.logo)
        
		# configure grid layout (3x4)
        self.grid_columnconfigure(0, weight=3, uniform="fred")
        self.grid_columnconfigure(1, weight=7, uniform="fred")
        self.grid_rowconfigure(0, weight=1, uniform="fred")

        '''image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image = CTkImage(Image.open(os.path.join(image_path, "light_conductor.png")), size=(26, 26))'''

        pages = (Page1, Page2, Page3)
        self.pages = (i for i in pages)
        self.current_page = next(self.pages)
        # self.current_page = next(self.pages)

        self.build_sidebar()
        self.build_main()
        
        if self.data.is_first_launch_of_app():
            WelcomeWindow(self, self.data)

    def build_sidebar(self):
        """creates a sidebar."""
        self.sidebar_frame = Sidebar(self, self.data, self.update_language, self.update_appearance_mode, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

    def build_main(self, session: Union[SessionData, None] = None):
        self.main_frame = self.current_page(self, data=self.data, session=session, command=self.next_page) # type: ignore
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        """
        settings_image = CTkImage(light_image=Image.open("light_settings.png"),
                             dark_image=Image.open("dark_settings.png"),
                             size=(25, 25))

        settings_button = CTkButton(self, text="", image=settings_image, command=settings_button_event)
        settings_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")"""
    
    def next_page(self, session: SessionData):
        try:
            self.main_frame.destroy()
            self.current_page = next(self.pages)
            self.build_main(session)
        except StopIteration:
            self.destroy()
    
    def update_language(self, language: str):
        if self.user_config.interface_language == language: # type: ignore
            return None
        
        self.user_config.interface_language = language # type: ignore
        UserConfigManager(self.main_folder).save_user_config(vars(self.user_config))

        session = self.main_frame.get_session_data()

        self.sidebar_frame.destroy()
        self.main_frame.destroy()
        self.build_sidebar()
        self.build_main(session)

    def update_appearance_mode(self, new_appearance_mode: str):
        if new_appearance_mode == self.user_config.appearance_mode: # type: ignore
            return 
        
        self.user_config.appearance_mode = new_appearance_mode # type: ignore
        UserConfigManager(self.main_folder).save_user_config(vars(self.user_config))
        
        set_appearance_mode(new_appearance_mode)
        
    def run(self):
        # функция для запуска приложения
        self.mainloop()



if __name__ == "__main__":
    app = App()
    app.run()