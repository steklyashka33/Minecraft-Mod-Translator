from typing import Optional, Tuple, Union
from customtkinter import *
from .get_data import GetData
import webbrowser
from sys import platform

class WelcomeWindow(CTkToplevel):
    """Open welcome window."""
    def __init__(self, master: any, 
                 data: GetData,
                 *args, fg_color: str | Tuple[str, str] | None = None, 
                 **kwargs):
        super().__init__(master, *args, fg_color=fg_color, **kwargs)
        self.config, _, self.lang, _ = data.get()

        self.title(self.lang.welcome)
        self.transient(master)
        self.grab_set()
        self.geometry("300x200")
        self.resizable(False, False)
        self.iconbitmap(self.config.logo)
        if platform.startswith("win"):
            self.after(200, lambda: self.iconbitmap(self.config.logo))
        # self.protocol("WM_DELETE_WINDOW", self.close_toplevel)
        # self.wm_iconbitmap()
        # self.after(300, lambda: self.iconphoto(False, self.iconpath))

        self.build()

    def close_toplevel(self):
        self.destroy()
            
    def build(self):
        label_title = CTkLabel(self, text=self.config.title, anchor="w", font=("Arial",20,"bold"))
        label_title.pack(fill="x", padx=10, pady=10)
        info = "Package finder for tkinter and  \n\nMade by Staklyashka"
        label_info = CTkLabel(self, text=info, anchor="w", justify="left")
        label_info.pack(fill="x", padx=10)
        
        repo_link = CTkLabel(self, text="Homepage", font=("Arial",13), text_color=["blue","cyan"])
        repo_link.pack(anchor="w", padx=10)
        
        repo_link.bind("<Button-1>", lambda event: webbrowser.open_new_tab(self.config.repository_link))
        repo_link.bind("<Enter>", lambda event: repo_link.configure(font=("Arial",13,"underline"), cursor="hand2"))
        repo_link.bind("<Leave>", lambda event: repo_link.configure(font=("Arial",13), cursor="arrow"))

        button_okey = CTkButton(self, text=self.lang.okey, command=self.close_toplevel)
        button_okey.pack(pady=10)
