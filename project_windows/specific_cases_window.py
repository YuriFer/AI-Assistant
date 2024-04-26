import customtkinter as tk
from project_windows.window import Window
from tkcalendar import DateEntry

class SpecificCasesWindow(Window):
    def __init__(self):
        super().__init__(title="Casos Específicos", dimension="550x550")

        self.specific_case_frame = tk.CTkFrame(self, width=120, corner_radius=0)
        self.specific_case_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.specific_case_frame.grid_rowconfigure(4, weight=1)

        self.specific_cases_label = tk.CTkLabel(self.specific_case_frame, text="Casos Específicos", font=tk.CTkFont(size=12, weight="bold"))
        self.specific_cases_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.specific_cases_city_label = tk.CTkLabel(self.specific_case_frame, text="Cidade:", anchor="w", font=tk.CTkFont(size=10, weight="bold"))
        self.specific_cases_city_label.grid(row=2, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.specific_cases_city_optionmenu = tk.CTkOptionMenu(self.specific_case_frame, values=["Araguari", "Uberlândia", "Uberaba"])
        self.specific_cases_city_optionmenu.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")

        self.specific_cases_disease_label = tk.CTkLabel(self.specific_case_frame, text="Arbovirose:", anchor="w", font=tk.CTkFont(size=10, weight="bold"))
        self.specific_cases_disease_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.specific_cases_disease_optionmenu = tk.CTkOptionMenu(self.specific_case_frame, values=["Dengue", "Zika", "Chikungunya"])
        self.specific_cases_disease_optionmenu.grid(row=5, column=0, padx=20, pady=(5, 10), sticky="ew")

        self.specific_cases_start_week_label = tk.CTkLabel(self.specific_case_frame, text="Mês inicial:", anchor="w", font=tk.CTkFont(size=10, weight="bold"))
        self.specific_cases_start_week_label.grid(row=6, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.specific_cases_start_week_optionmenu = tk.CTkOptionMenu(self.specific_case_frame, values=["Janeiro", "Fevereiro", "Março"])
        self.specific_cases_start_week_optionmenu.grid(row=7, column=0, padx=20, pady=(5, 10), sticky="ew")

        self.specific_cases_end_week_label = tk.CTkLabel(self.specific_case_frame, text="Mês final:", anchor="w", font=tk.CTkFont(size=10, weight="bold"))
        self.specific_cases_end_week_label.grid(row=8, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.specific_cases_end_week_optionmenu = tk.CTkOptionMenu(self.specific_case_frame, values=["Janeiro", "Fevereiro", "Março"])
        self.specific_cases_end_week_optionmenu.grid(row=9, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.specific_case_calendar_frame = tk.CTkFrame(self, width=200, corner_radius=0)
        self.specific_case_calendar_frame.grid(row=0, column=1, sticky="w")

        self.specific_case_calendar = DateEntry(self.specific_case_calendar_frame, date_pattern="yyyy-mm-dd")
        self.specific_case_calendar.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="ew")

        self.mainloop()
        