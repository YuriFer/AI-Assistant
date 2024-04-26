import os
import requests


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