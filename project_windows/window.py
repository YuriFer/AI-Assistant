import os

import customtkinter as tk

tk.set_appearance_mode("Dark")
tk.set_default_color_theme("dark-blue")

class Window(tk.CTk):
    def __init__(self, title="New Window", dimension="1100x580"):
        super().__init__()
        self.logged_user = os.getlogin()
        self.configure_window(title, dimension)
        self.window_exist = True

    def configure_window(self, title:str, dimension:str):
        self.title(f"{title} - Usuário: {self.logged_user}")
        self.geometry(dimension)
        self.iconbitmap("assets/AI-Assistant.ico")
        self.width = int(dimension.split("x")[0])
        self.height = int(dimension.split("x")[1])
        self.centralize_window(dimension)
    
    def centralize_window(self, dimension, value:int=0):
        self.update_idletasks()
        pos_x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        pos_y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry(f"{dimension}+{pos_x + value}+{pos_y}")
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        tk.set_appearance_mode(new_appearance_mode.split(" ")[0].lower())