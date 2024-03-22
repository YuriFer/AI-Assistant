import sys
import os
import pathlib

import customtkinter as tk

sys.path.append(str(pathlib.Path(__file__).parent.parent))
from project_windows.window import Window

class AiAssistant(Window):
    def __init__(self):
        super().__init__(title="Principal")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = tk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.logo_label = tk.CTkLabel(self.sidebar_frame, text="Assistente Informativo", font=tk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = tk.CTkLabel(self.sidebar_frame, text="Tema da Tela:", anchor="w", font=tk.CTkFont(size=12, weight="bold"))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        self.appearance_mode_optionemenu = tk.CTkOptionMenu(self.sidebar_frame, values=["Dark Mode", "Light Mode"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 15), sticky="ew")

        # create textbox
        self.textbox = tk.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")

        # create main entry and button
        self.entry = tk.CTkEntry(self, placeholder_text="Digite a sua pergunta...", font=tk.CTkFont(size=12))
        self.entry.grid(row=3, column=1, padx=(20, 20), pady=(20, 20), sticky="ew")

        self.main_button_1 = tk.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=1, padx=(20, 40), pady=(20, 20), sticky="e")

if __name__ == "__main__":
    app = AiAssistant()
    app.mainloop()




