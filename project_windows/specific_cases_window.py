import customtkinter as tk

from unidecode import unidecode

from project_windows.window import Window
from project_windows.graph_window import GraphWindow
from tkcalendar import DateEntry

from dengue_api_consult import ApiRequestObject, DengueApiService

class SpecificCasesWindow(Window):

    def __init__(self, textbox:tk.CTkTextbox):
        super().__init__(title="Casos Específicos", dimension="650x550")
        self.textbox = textbox

        self.graph_window = None
        self.dengue_service = DengueApiService()
        
        self.resizable(False, False)
        self.cities = DengueApiService.load_cities(self)

        self.frame = tk.CTkFrame(self, corner_radius=0, border_width=2)
        self.frame.grid(columnspan = 3, rowspan=4, sticky="nsew")

        self.label = tk.CTkLabel(self.frame, text="Casos Específicos", font=tk.CTkFont(size=14, weight="bold"))
        self.label.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.filter_label = tk.CTkLabel(self.frame, text="Filtro Cidades", font=tk.CTkFont(size=12, weight="bold"))
        self.filter_label.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.city_filter = tk.CTkEntry(self.frame, font=tk.CTkFont(size=12), placeholder_text="Digite o nome da cidade...")
        self.city_filter.grid(row=2, column=1, padx=20, pady=(5, 10), sticky="ew")
        self.city_filter.bind("<KeyRelease>", self.filter_cities)

        self.city_label = tk.CTkLabel(self.frame, text="Cidade:", anchor="w", font=tk.CTkFont(size=12, weight="bold"))
        self.city_label.grid(row=3, column=1, padx=20, pady=(10, 0), sticky="ew")
        
        self.city_optionmenu = tk.CTkOptionMenu(self.frame, values=self.cities, dynamic_resizing=False, width=250)
        self.city_optionmenu.grid(row=4, column=1, padx=20, pady=(5, 10))

        self.disease_label = tk.CTkLabel(self.frame, text="Arbovirose:", anchor="w", font=tk.CTkFont(size=12, weight="bold"))
        self.disease_label.grid(row=5, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.disease_optionmenu = tk.CTkOptionMenu(self.frame, values=["Dengue", "Zika", "Chikungunya"])
        self.disease_optionmenu.grid(row=6, column=1, padx=20, pady=(5, 10), sticky="ew")

        self.start_week_label = tk.CTkLabel(self.frame, text="Data inicial:", anchor="w", font=tk.CTkFont(size=12, weight="bold"))
        self.start_week_label.grid(row=7, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.start_week_date = DateEntry(self.frame, font=tk.CTkFont(size=10), date_pattern="dd/mm/yyyy")
        self.start_week_date.grid(row=8, column=1, padx=20, pady=(5, 10), sticky="ew")           

        self.end_week_label = tk.CTkLabel(self.frame, text="Data final:", anchor="w", font=tk.CTkFont(size=12, weight="bold"))
        self.end_week_label.grid(row=9, column=1, padx=20, pady=(10, 0), sticky="ew")

        self.end_week_date = DateEntry(self.frame, font=tk.CTkFont(size=10), date_pattern="dd/mm/yyyy")
        self.end_week_date.grid(row=10, column=1, padx=20, pady=(5, 20), sticky="ew")

        self.send_button = tk.CTkButton(self.frame, text="Enviar", font=tk.CTkFont(size=12, weight="bold"), command=self.call_info_api)
        self.send_button.grid(row=12, column=0, padx=20, pady=(60, 20), sticky="nsew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        self.window_exist = False
        self.destroy()

    def filter_cities(self, event):
        query = unidecode(self.city_filter.get().lower())

        filtered_cities = [city for city in self.cities if query in unidecode(city.lower())]
        self.update_optionmenu(filtered_cities)

    def update_optionmenu(self, values):
        if self.city_filter.get() != "":
            self.city_optionmenu.set(values[0] if values else "")
            self.city_optionmenu.configure(values=values)
            return
        self.city_optionmenu.set(self.cities[0] if self.cities else "")
        self.city_optionmenu.configure(values=self.cities)

    def get_values(self):
        city = self.city_optionmenu.get().split(" - ")[0].strip()
        disease = self.disease_optionmenu.get().lower()
        start_week = self.dengue_service.date_to_week(self.start_week_date.get_date())
        end_week = self.dengue_service.date_to_week(self.end_week_date.get_date())
        year_start= self.dengue_service.get_year(self.start_week_date.get_date())
        year_end= self.dengue_service.get_year(self.end_week_date.get_date())
        
        return city, disease, start_week, end_week, year_start, year_end
    
    def get_graph_values(self, response:list):
        data = {
            "weeks": [],
            "cases_est": [],
            "cases": [],
            "population": 0
        }
        for line in response:
            data["weeks"].append(self.dengue_service.miliseconds_to_date(line["data_iniSE"])[:5])
            data["cases_est"].append(line["casos_est"])
            data["cases"].append(line["casos"])
            data["population"] = line["pop"]
        
        return data

    
    def call_info_api(self):
        city, disease, start_week, end_week, year_start, year_end = self.get_values()
        api_request = ApiRequestObject(
            geocode=city,
            week_start=start_week,
            week_end=end_week,
            year_start=year_start,
            year_end=year_end,
            disease=disease
        )
        response = DengueApiService().call_dengue_api(api_request)

        graph_values = self.get_graph_values(response)

        if self.graph_window is None:
            self.instance_graph(graph_values)
        else:
            if self.graph_window.window_exist:
                self.graph_window.lift()
            else:
                self.instance_graph(graph_values)

        return response
    
    def instance_graph(self, graph_values):
        self.graph_window = GraphWindow(graph_values)
        self.graph_window.centralize_window("650x550", 500)
        self.graph_window.mainloop()