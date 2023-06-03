from customtkinter import *
from PIL import Image


set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue")

title = "Evolutionary widget test"

class App(CTk):
    def __init__(self):
        super().__init__()

        # создание главного окна
        self.title(title)
        window_width = 480
        window_height = 360
        self.geometry(f"{window_width}x{window_height}")

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
        self.image = CTkImage(Image.open(os.path.join(image_path, "light_conductor.png")), size=(26, 26))

class MyButton(CTkFrame):
    pass



if __name__ == "__main__":
    app = App()
    app.mainloop()