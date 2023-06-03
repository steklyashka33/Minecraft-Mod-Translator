import tkinter as tk
from customtkinter import *
from CTkScrollableDropdown import CTkScrollableDropdown
from PIL import Image

#pip install pillow
#pip install pyyaml
#pip install babel

set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

title = "Mod Translator"

class App(CTk):
    def __init__(self):
        super().__init__()

        # создание главного окна
        self.title(title)
        window_width = 480
        window_height = 360

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

        self.set_values("Russian")



    def build_sidebar(self):
        #
        self.sidebar_frame = CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        # 
        self.logo_label = CTkLabel(self.sidebar_frame, text=title, font=CTkFont(size=17, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=10, pady=(20, 10))

        # 
        self.interface_language_label = CTkLabel(self.sidebar_frame, anchor="w")
        self.interface_language_label.grid(row=2, column=0, padx=10, pady=(10, 0))
        self.interface_language_menu = CTkOptionMenu(self.sidebar_frame, width=80, command=self.reset_values)
        self.interface_language_menu.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        def change_appearance_mode_event(new_appearance_mode: str):
            set_appearance_mode(new_appearance_mode)
        # 
        self.appearance_mode_label = CTkLabel(self.sidebar_frame, anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = CTkOptionMenu(self.sidebar_frame, width=80, command=change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10), sticky="ew")



    def build_main(self):
        self.main_frame = CTkFrame(self)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        self.main_frame.grid_columnconfigure(0, weight=1, uniform="fred")
        self.main_frame.grid_rowconfigure((1, 2, 3, 4), weight=6, uniform="fred")
        self.main_frame.grid_rowconfigure((0, 5), weight=10, uniform="fred")

        # 
        label_font = CTkFont("Arial", size=28, weight="bold")
        self.main_label = CTkLabel(self.main_frame, font=label_font) #text="Ввод данных"
        self.main_label.grid(row=0, column=0, columnspan=3, pady=10)

        # создание подписи к entry
        entry_label = CTkLabel(self.main_frame, text="Введите путь к папке с модами:")
        entry_label.grid(row=1, column=0, sticky="s")
        
        # создание entry для ввода пути к папке
        self.directory_path = StringVar()
        self.folder_entry = MyEntry(self.main_frame, textvariable=self.directory_path, placeholder_text="", image=self.image)
        #self.folder_entry = CTkEntry(self.main_frame, textvariable=self.directory_path, placeholder_text="")
        self.folder_entry.grid(row=2, column=0)

        # создание подписи к entry
        language_label = CTkLabel(self.main_frame, text="Язык перевода:")
        language_label.grid(row=3, column=0, sticky="s")
        
        # создание виджета CTkOptionMenu для выбора языков
        self.target_language = StringVar()
        self.language_optionmenu = CTkOptionMenu(self.main_frame)
        self.language_optionmenu.grid(row=4, column=0)
        CTkScrollableDropdown(self.language_optionmenu, values=self.target_language)
        
        # создание кнопки для продолжения
        next_button = CTkButton(self.main_frame, text="Продолжить", command=self.next_step)
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
        

        """
    
    def build_folder_entry(self):
        # создание frame для разделения строчки на 3/5
        frame_folder_entry = CTkFrame(self, fg_color="transparent")
        frame_folder_entry.grid(row=1, column=0, columnspan=3, sticky="nsew")
        frame_folder_entry.grid_columnconfigure((0,2), weight=1, uniform="fred")
        frame_folder_entry.grid_columnconfigure(1, weight=4, uniform="fred")
        frame_folder_entry.grid_rowconfigure((0,1,2), weight=1, uniform="fred")

        # создание image проводника
        image = CTkImage(light_image=Image.open("light_conductor.png"),
                             dark_image=Image.open("dark_conductor.png"),
                             size=(25, 25))

        # создание button
        button = CTkButton(entry_frame, width=25, height=25, corner_radius=5, text="", image=image, command=self.choose_folder)
        button.pack(side=LEFT)"""
    
    def set_values(self, language):
        self.interface_language_menu.configure(values=["Russian", "English"])
        self.interface_language_menu.set("Russian")
        self.language_optionmenu.configure(values=["Русский", "English"])
        self.appearance_mode_optionemenu.set("System")

        self.reset_values(language)
    
    def reset_values(self, language):
        self.interface_language_label.configure(text="Interface Language:")
        self.appearance_mode_label.configure(text="Appearance Mode:")
        self.appearance_mode_optionemenu.configure(values=["Light", "Dark", "System"])

        self.main_label.configure(text="Ввод данных")
        if self.target_language.get() not in ["Русский", "English"]: self.language_optionmenu.set("Выберите язык")
        
    def choose_folder(self):
        # функция для вызова диалога выбора папки
        folder_path = filedialog.askdirectory()
        self.directory_path.set(folder_path)
        
    def next_step(self):
        # функция, которая будет вызываться при нажатии на кнопку "Продолжить"
        print(self.directory_path.get())
        for widget in self.winfo_children():
            widget.destroy()
        
    def run(self):
        # функция для запуска приложения
        self.mainloop()




import tkinter
from typing import Union, Tuple, Optional
class MyEntry(CTkEntry):
    def __init__(self,
                 master: any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 placeholder_text_color: Optional[Union[str, Tuple[str, str]]] = None,

                 textvariable: Union[tkinter.Variable, None] = None,
                 placeholder_text: Union[str, None] = None,
                 font: Optional[Union[tuple, CTkFont]] = None,
                 image: Union[CTkImage, "ImageTk.PhotoImage", None] = None,
                 state: str = tkinter.NORMAL,
                 **kwargs):
        
        width -= height
        
        self._button_color = ThemeManager.theme["CTkOptionMenu"]["button_color"] if button_color is None else self._check_color_type(button_color)
        self._button_hover_color = ThemeManager.theme["CTkOptionMenu"]["button_hover_color"] if button_hover_color is None else self._check_color_type(button_hover_color)

        super().__init__(master, width, height, corner_radius, border_width, 
                         bg_color, fg_color, border_color, text_color, placeholder_text_color, 
                         textvariable, placeholder_text, font, state, **kwargs)
        
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(0, weight=1)

        image.configure(size=(16, 16))
        
        self._button_canvas = CTkCanvas(master=self,
                                 highlightthickness=0,
                                 width=self._apply_widget_scaling(self._current_width),
                                 height=self._apply_widget_scaling(self._current_height-20))
        self._button_draw_engine = DrawEngine(self._canvas)

        

        self._button = CTkLabel(self,
                                 width=self._apply_widget_scaling(self._desired_height),
                                 height=self._apply_widget_scaling(self._desired_height-7),
                                 text="", 
                                 image=image, )
        self._button.bind("<Button-1>", lambda x: print(self._apply_widget_scaling(self._desired_height), self.winfo_height()))
        #self._button.grid(row=0, column=1)

    def _draw(self, no_color_updates=False):
        super()._draw()

        requires_recoloring = self._draw_engine.draw_rounded_rect_with_border(self._apply_widget_scaling(self._current_width),
                                                                              self._apply_widget_scaling(self._current_height),
                                                                              self._apply_widget_scaling(self._corner_radius),
                                                                              self._apply_widget_scaling(self._border_width))

        if requires_recoloring or no_color_updates is False:
            self._canvas.itemconfig("inner_parts_right",
                                    outline=self._apply_appearance_mode(self._button_color),
                                    fill=self._apply_appearance_mode(self._button_color))


if __name__ == "__main__":
    app = App()
    app.run()
