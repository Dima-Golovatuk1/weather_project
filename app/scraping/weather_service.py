import httpx
import asyncio
from app.core.config import settings


class WeatherScraper:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    async def get_current_weather(city: str = "Обухів", lang: str = "ua"):
        params = {
            "q": city,
            "appid": settings.API_KEY_WEATHER,
            "units": "metric",
            "lang": lang
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(WeatherScraper.BASE_URL, params=params)

        response.raise_for_status()

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


if __name__ == "__main__":
    weather_test = WeatherScraper()
    print(asyncio.run(weather_test.get_current_weather()))
