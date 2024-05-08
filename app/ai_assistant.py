import datetime
import sys
import os
import pathlib

import customtkinter as tk

sys.path.append(str(pathlib.Path(__file__).parent.parent))
sys.path.append(str(pathlib.Path(__file__).parent.parent / "prompts"))
sys.path.append(str(pathlib.Path(__file__).parent.parent / "dao"))
from project_windows.window import Window
from project_windows.specific_cases_window import SpecificCasesWindow
from service.open_ai import OpenAIService

class AiAssistant(Window):
    def __init__(self):
        super().__init__(title="Principal")
        
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.sidebar_frame = tk.CTkFrame(self, width=140, corner_radius=0, border_width=2)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = tk.CTkLabel(self.sidebar_frame, text="Assistente Informativo\nSobre a Dengue", font=tk.CTkFont(size=18, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.specific_cases_button = tk.CTkButton(self.sidebar_frame, text="Casos Específicos",anchor="w", font=tk.CTkFont(size=12, weight="bold"), command=SpecificCasesWindow)
        self.specific_cases_button.grid(row=3, column=0, padx=20, pady=(5, 15), sticky="ew")

        self.appearance_mode_label = tk.CTkLabel(self.sidebar_frame, text="Tema da Tela:", anchor="w", font=tk.CTkFont(size=12, weight="bold"))
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.appearance_mode_optionemenu = tk.CTkOptionMenu(self.sidebar_frame, values=["Dark Mode", "Light Mode"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(5, 15), sticky="ew")

        # create textbox
        self.textbox = tk.CTkTextbox(self, width=250, wrap="word", font=tk.CTkFont(size=12))
        self.textbox.grid(row=0, column=1, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.textbox.configure(state="disabled")

        # create entry and button frame
        self.entry_button_frame = tk.CTkFrame(self, corner_radius=20)
        self.entry_button_frame.grid(row=3, column=1, padx=(20, 20), pady=(20, 10), sticky="ew")

        self.entry_button_frame.grid_columnconfigure(1, weight=1)
        self.entry_button_frame.grid_columnconfigure((2, 3), weight=0)

        # create main entry and button
        self.entry = tk.CTkEntry(self.entry_button_frame, placeholder_text="Digite a sua pergunta...", font=tk.CTkFont(size=12))
        self.entry.grid(row=3, column=1, padx=(20, 10), pady=(20, 20), sticky="nsew")

        self.main_button_1 = tk.CTkButton(self.entry_button_frame, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Enviar", font=tk.CTkFont(size=12), command=self.send_question)
        self.main_button_1.grid(row=3, column=2, padx=(10, 20), pady=(20, 20), sticky="nsew")

    def get_text(self, widget):
        value = widget.get() if widget.get() else None
        widget.delete(0, "end")
        return value
    
    def send_question(self):
        user_message = self.get_text(self.entry)
        response = OpenAIService().initiate_context(user_message, widget=self.textbox)

        self.response_register(user_message, response)

    def response_register(self, user_message:str, response:OpenAIService):
        response_backup = {
            "date": datetime.datetime.now().replace(hour=0, minute=0, second=0).strftime("%d/%m/%Y"),
            "message": user_message,
            "response": response.response
        }


if __name__ == "__main__":
    app = AiAssistant()
    app.mainloop()




