import tkinter as tk
from customtkinter import *
from PIL import Image

set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")


class App(CTk):
    def __init__(self):
        super().__init__()

        # создание главного окна
        self.title("Mod Translator")
        self.geometry(f"{400}x{300}")
        self.resizable(0, 0)
        
		# configure grid layout (3x4)
        self.grid_columnconfigure((0, 2), weight=1, uniform="fred")
        self.grid_columnconfigure((1), weight=5, uniform="fred")
        self.grid_rowconfigure(0, weight=1, uniform="fred")
        self.grid_rowconfigure(1, weight=5, uniform="fred")

        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, rowspan=2, column=1, pady=20, sticky="nsew")
        
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="fred")
        self.main_frame.grid_rowconfigure((1, 2, 3), weight=3, uniform="fred")
        self.main_frame.grid_rowconfigure(0, weight=4, uniform="fred")

        CTkFrame(self).grid(row=0, column=2)
        CTkFrame(self.main_frame, width=300).grid(row=0, column=0)
        CTkFrame(self.main_frame, width=300).grid(row=2, column=0)
        # 
        label_font = CTkFont("Arial", size=28, weight="bold")
        main_label = CTkLabel(self.main_frame, text="Ввод данных", font=label_font)
        main_label.grid(row=0, column=0, columnspan=3, pady=10)

        """def button_click_event():
            dialog = CTkInputDialog(text="Type in a number:", title="Test")
            print("Number:", dialog.get_input())


        button = CTkButton(self, text="Open Dialog", command=button_click_event)
        button.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # 
        label_font = CTkFont("Arial", size=28, weight="bold")
        main_label = CTkLabel(self, text="Ввод данных", font=label_font)
        main_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="s")

        # создание виджетов для ввода пути к папке
        self.build_folder_entry()
        
        # переменная для хранения выбранного языка
        self.target_language = StringVar()
        
        # создание виджета CTkOptionMenu для выбора языков
        language_optionmenu = CTkOptionMenu(self, variable=self.target_language, values=["Русский", "English"])
        language_optionmenu.grid(row=2, column=1)
        language_optionmenu.set("Выберите язык")
        
        # создание кнопки для продолжения
        next_button = CTkButton(self, text="Продолжить", command=self.next_step)
        next_button.grid(row=3, column=1)
        
        # создание виджета CTkOptionMenu для выбора языка интерфейса
        self.interface_language = CTkOptionMenu(self, width=96, height=24, values=["Русский", "English"])
        self.interface_language.grid(row=0, column=2, padx=8, pady=10, sticky="ne")
        self.interface_language.set("Русский")
    
    def build_folder_entry(self):
        # создание frame для разделения строчки на 3/5
        frame_folder_entry = CTkFrame(self, fg_color="transparent")
        frame_folder_entry.grid(row=1, column=0, columnspan=3, sticky="nsew")
        frame_folder_entry.grid_columnconfigure((0,2), weight=1, uniform="fred")
        frame_folder_entry.grid_columnconfigure(1, weight=4, uniform="fred")
        frame_folder_entry.grid_rowconfigure((0,1,2), weight=1, uniform="fred")

        # создание подписи к entry
        entry_label = CTkLabel(frame_folder_entry, text="Введите путь к папке с модами:")
        entry_label.grid(row=0, column=1, sticky="w")

        # создание frame для виджетов
        entry_frame = CTkFrame(frame_folder_entry)
        entry_frame.grid(row=1, column=1, sticky="nsew")

        # переменная написанного текста entry
        self.directory_path = StringVar()

        # создание entry для ввода пути к папке
        self.folder_entry = CTkEntry(entry_frame, textvariable=self.directory_path, placeholder_text="")
        self.folder_entry.pack(side=LEFT, fill=BOTH, expand=True)

        # создание image проводника
        image = CTkImage(light_image=Image.open("light_conductor.png"),
                             dark_image=Image.open("dark_conductor.png"),
                             size=(25, 25))

        # создание button
        button = CTkButton(entry_frame, width=25, height=25, corner_radius=5, text="", image=image, command=self.choose_folder)
        button.pack(side=LEFT)
        
    def choose_folder(self):
        # функция для вызова диалога выбора папки
        folder_path = filedialog.askdirectory()
        self.directory_path.set(folder_path)"""
        
    def next_step(self):
        # функция, которая будет вызываться при нажатии на кнопку "Продолжить"
        print(self.directory_path.get())
        for widget in self.winfo_children():
            widget.destroy()
        
    def run(self):
        # функция для запуска приложения
        self.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
