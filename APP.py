from customtkinter import *
from utils import *
from pages import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
import os


class App(CTk):
    def __init__(self):
        super().__init__()

        self.main_folder = os.path.dirname(os.path.abspath(__file__))
        self.data = GetData(self.main_folder)
        
        self.config, self.user_config, self.lang, self.supported_languages = self.data.get()

        # создание главного окна
        self.title( self.config["title"] )
        window_width = 600
        window_height = 450

        set_appearance_mode(self.user_config["appearance_mode"])  # Modes: "System" (standard), "Dark", "Light"
        set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = (screen_width - window_width)//2
        y_cordinate = (screen_height - window_height)//2
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        #self.resizable(0, 0)
        
		# configure grid layout (3x4)
        self.grid_columnconfigure(0, weight=3, uniform="fred")
        self.grid_columnconfigure(1, weight=7, uniform="fred")
        self.grid_rowconfigure(0, weight=1, uniform="fred")

        '''image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image = CTkImage(Image.open(os.path.join(image_path, "light_conductor.png")), size=(26, 26))'''

        self.build_sidebar()
        self.build_main()



    def build_sidebar(self):
        self.config, self.user_config, self.lang, self.supported_languages = self.data.get()
        
        #
        self.sidebar_frame = CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # 
        self.logo_label = CTkLabel(self.sidebar_frame, text=self.config["title"], font=CTkFont(size=21, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        font_label=CTkFont(size=15)

        # 
        values = list(self.user_config["dict_interface_language"].keys())
        self.interface_language_label = CTkLabel(self.sidebar_frame, text=self.lang["label_interface_language"], anchor="w", font=font_label)
        self.interface_language_label.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.interface_language_menu = CTkOptionMenu(self.sidebar_frame, values=values, command=self.language_change)
        self.interface_language_menu.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        self.interface_language_menu.set(self.lang["language_name"])

        # 
        system_list_of_appearance_modes = self.config["system_list_of_appearance_modes"]
        lang_list_of_appearance_modes = self.lang["list_of_appearance_modes"]
        self.dict_of_appearance_modes = dict(zip(lang_list_of_appearance_modes, system_list_of_appearance_modes))
        dict_of_system_appearance_modes = dict(zip(system_list_of_appearance_modes, lang_list_of_appearance_modes))
        self.appearance_mode_label = CTkLabel(self.sidebar_frame, text=self.lang["label_appearance_mode"], anchor="w", font=font_label)
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, values=self.lang["list_of_appearance_modes"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10), sticky="ew")
        self.appearance_mode_optionemenu.set(dict_of_system_appearance_modes[ self.user_config["appearance_mode"] ])



    def build_main(self):
        self.main_frame = Page1(self, GetData(self.main_folder))
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        """
        settings_image = CTkImage(light_image=Image.open("light_settings.png"),
                             dark_image=Image.open("dark_settings.png"),
                             size=(25, 25))

        settings_button = CTkButton(self, text="", image=settings_image, command=settings_button_event)
        settings_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")"""
    
    def language_change(self, language: str):
        if self.user_config["interface_language"] == language:
            return None
        
        self.user_config["interface_language"] = language
        UserConfigManager(self.main_folder).save_user_config(self.user_config)

        session = self.main_frame.get_session_data()

        self.sidebar_frame.destroy()
        self.main_frame.destroy()
        self.build_sidebar()
        self.build_main()

        self.main_frame.set_session_data(session)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        system_new_appearance_modes = self.dict_of_appearance_modes[new_appearance_mode]
        
        if system_new_appearance_modes == self.user_config["appearance_mode"]:
            return None
        
        self.user_config["appearance_mode"] = system_new_appearance_modes
        UserConfigManager(self.main_folder).save_user_config(self.user_config)
        
        set_appearance_mode(system_new_appearance_modes)
        
    def run(self):
        # функция для запуска приложения
        self.mainloop()

def Start():
    app = App()
    app.run()
    del app

if __name__ == "__main__":
    Start()