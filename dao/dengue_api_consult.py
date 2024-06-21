import os
import requests
import json
from datetime import datetime

from unidecode import unidecode


class ApiRequestObject:
    def __init__(
            self, 
            geocode: int,
            week_start: int,
            week_end: int,
            year_start: int,
            year_end: int,
            disease:str = "dengue",
            format:str = "json"
            ):
        self.geocode = geocode
        self.week_start = week_start
        self.week_end = week_end
        self.year_start = year_start
        self.year_end = year_end
        self.disease = disease
        self.format = format
        self.params = f"geocode={geocode}&disease={disease}&format={format}&ew_start={week_start}&ew_end={week_end}&ey_start={year_start}&ey_end={year_end}"
        self.url = os.getenv("DENGUE_API_URL")

class DengueApiService:
    def call_dengue_api(self, api_request: ApiRequestObject):
        response = requests.get(api_request.url, params=api_request.params)
        if response.status_code == 200:
            return response.json()
        return None
    
    def load_cities(self, specific_city:str = None) -> list:
        cities = []
        with open('assets\cities_data.json', 'r', encoding='utf-8-sig') as file:
            data = json.load(file)

            for city in data:
                if specific_city:
                    if unidecode(specific_city.lower()) in unidecode(city["nome_municipio"].lower()):
                        return city["cod_municipio"]
                cities.append(f'{city["cod_municipio"]} - {city["nome_municipio"]}')
        return cities
    
    def date_to_week(self, date:datetime):
        week = date.isocalendar()[1]
        return week
    
    def get_year(self, date:datetime):
        year = date.year
        return year
    
    def miliseconds_to_date(self, miliseconds):
        return datetime.fromtimestamp(miliseconds / 1000.0).strftime("%d/%m/%Y")
    
    def transform_date(self, start_date:str, end_date:str):
        start_date = datetime.strptime(start_date, "%d/%m/%Y")
        end_date = datetime.strptime(end_date, "%d/%m/%Y") 

        start_week = self.date_to_week(start_date)
        end_week = self.date_to_week(end_date)
        start_year = self.get_year(start_date)
        end_year = self.get_year(end_date)
        return start_week, end_week, start_year, end_year
    
    def manipulate_data(self, data:list, city):
        final_data = []

        for line in data:
            new_data = {}
            new_data["data_iniSE"] = self.miliseconds_to_date(line["data_iniSE"])
            new_data["casos_est"] = line["casos_est"]
            new_data["casos"] = line["casos"]
            new_data["nivel"] = line["nivel"]
            new_data["populacao"] = line["pop"]
            new_data["cidade"] = city

            final_data.append(new_data)
            
        return final_data