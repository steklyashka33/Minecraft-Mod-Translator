__author__ = 'Steklyashka'

name = "ModTranslator"
from customtkinter import *

set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CustomTkinter")
        self.geometry(f"{400}x{300}")
        self.minsize(400, 300)
        
		# configure grid layout (3x4)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Create frame and widgets
        language_change = CTkOptionMenu(self, values=["English", "Russian"])
        language_change.grid(row=0, column=2)
        target_language = CTkOptionMenu(self, values=["English", "Русский"])
        target_language.grid(row=2, column=1)
        next_button = CTkButton(self, text="Next", )
        next_button.grid(row=3, column=2, sticky="e")

        #CTkFrame(self, fg_color='black').grid(row=0, column=0)
        #CTkFrame(self, fg_color='green').grid(row=1, column=0)
        #CTkFrame(self, fg_color='black').grid(row=2, column=0)
        
if __name__ == '__main__':
    app = App()
    app.mainloop()
