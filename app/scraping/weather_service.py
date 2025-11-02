import requests
from app.core.config import settings

class WeatherScraper:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self, city: str = "Обухів", lang: str = "ua"):
        params = {
            "q": city,
            "appid": settings.API_KEY_WEATHER,
            "units": "metric",
            "lang": lang
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        return {
            "city": city,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "main": data["weather"][0]["main"],
            "pressure": data["main"]["pressure"]
        }


weathertest = WeatherScraper()

print(weathertest.get_current_weather(lang="en"))
