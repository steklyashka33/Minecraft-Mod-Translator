from customtkinter import *
from utils import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
from multiprocessing import Process
import os


#pip install pillow
#pip install pyyaml
#pip install babel

set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

title = "Mod Translator"

class App(CTk):
    def __init__(self):
        super().__init__()

        self.main_folder = os.path.dirname(os.path.abspath(__file__))
        
        self.config = YAMLFileManager(self.main_folder, "config.yaml").load_file()
        folder_with_translations = self.config["folder_with_translations"]
        self.user_config = UserConfigManager(self.main_folder).get_user_config(folder_with_translations)
        language_file = self.user_config["dict_interface_language"][ self.user_config["interface_language"] ]
        self.lang = YAMLFileManager(os.path.join( self.main_folder, folder_with_translations ), language_file).load_file()

        # создание главного окна
        self.title( self.config["title"] )
        window_width = 600
        window_height = 450

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
        #self.grid_rowconfigure(1, weight=5, uniform="fred")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image = CTkImage(Image.open(os.path.join(image_path, "light_conductor.png")), size=(26, 26))

        self.build_sidebar()
        self.build_main()



    def build_sidebar(self):
        #
        self.sidebar_frame = CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # 
        self.logo_label = CTkLabel(self.sidebar_frame, text=title, font=CTkFont(size=21, weight="bold"))
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
        self.appearance_mode_label = CTkLabel(self.sidebar_frame, text=self.lang["label_appearance_mode"], anchor="w", font=font_label)
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, values=self.lang["list_of_appearance_modes"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10), sticky="ew")



    def build_main(self):
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="fred")
        self.main_frame.grid_rowconfigure((1, 2, 3, 4), weight=6, uniform="fred")
        self.main_frame.grid_rowconfigure((0, 5), weight=10, uniform="fred")

        # 
        header_font = CTkFont("Arial", size=38, weight="bold")
        self.main_label = CTkLabel(self.main_frame, text=self.lang["label_data_entry"], font=header_font)
        self.main_label.grid(row=0, column=0, columnspan=3, pady=10)

        label_font = CTkFont("Arial", size=18)
        widget_font = CTkFont("Arial", size=16)
        widget_width = 192
        widget_height = 36

        # создание подписи к вводу пути к папке
        entry_label = CTkLabel(self.main_frame, text=self.lang["label_enter_path"], font=label_font)
        entry_label.grid(row=1, column=0, sticky="s")
        
        # создание CTkComboBox для ввода пути к папке
        self.directory_path = StringVar()
        self.folder_entry = CTkComboBox(self.main_frame,  width=widget_width, height=widget_height, font=widget_font, variable=self.directory_path)
        self.folder_entry.grid(row=2, column=0)

        # создание подписи для выбора языков
        language_label = CTkLabel(self.main_frame, text=self.lang["label_translation_language"], font=label_font)
        language_label.grid(row=3, column=0, sticky="s")
        
        # создание виджета CTkOptionMenu для выбора языков
        self.target_language = StringVar()
        self.language_optionmenu = CTkOptionMenu(self.main_frame, width=widget_width, height=widget_height, font=widget_font, variable=self.target_language)
        self.language_optionmenu.grid(row=4, column=0)
        self.language_optionmenu.set(self.lang["label_Select_language"])
        CTkScrollableDropdown(self.language_optionmenu, height = 200, values=["Русский", "English"], frame_corner_radius=20)
        
        # создание кнопки для продолжения
        next_button = CTkButton(self.main_frame, width=widget_width, height=widget_height, font=widget_font, text=self.lang["label_next"], command=self.next_step)
        next_button.grid(row=5, column=0)

        """
            if self.settings_are_open:
                self.settings_frame.grid(row=0, rowspan=2, column=1, pady=20, sticky="nsew")
                self.main_frame.grid_forget()
            else:
                self.main_frame.grid(row=0, rowspan=2, column=1, pady=20, sticky="nsew")
                self.settings_frame.grid_forget()

        # создание image проводника
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

        self.destroy()
        Start()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        system_list_of_appearance_modes = self.config["system_list_of_appearance_modes"]
        lang_list_of_appearance_modes = self.lang["list_of_appearance_modes"]
        dict_of_appearance_modes = dict(zip(lang_list_of_appearance_modes, system_list_of_appearance_modes))
        system_new_appearance_modes = dict_of_appearance_modes[new_appearance_mode]
        
        if system_new_appearance_modes == self.user_config["appearance_mode"]:
            return None
        
        self.user_config["appearance_mode"] = system_new_appearance_modes
        UserConfigManager(self.main_folder).save_user_config(self.user_config)
        
        set_appearance_mode(new_appearance_mode)
        
    def choose_folder(self):
        # функция для вызова диалога выбора папки
        folder_path = filedialog.askdirectory()
        self.directory_path.set(folder_path)
        
    def next_step(self):
        # функция, которая будет вызываться при нажатии на кнопку "Продолжить"
        print(self.directory_path.get())
        for widget in self.winfo_children():
            widget.destroy()
            
        self.destroy()
        app = App()
        app.run()
        
    def run(self):
        # функция для запуска приложения
        self.mainloop()

def Start():
    app = App()
    app.run()
    del app

if __name__ == "__main__":
    Start()