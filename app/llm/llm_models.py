import asyncio
from app.core.llm_client import LLM
from app.core.config import settings
from app.scraping.weather_service import WeatherScraper

weather = WeatherScraper

from google import genai

class GeminiLLM(LLM):


    def __init__(self):
        self.__client = genai.Client(api_key=settings.API_KEY_AI)

    async def generate_al_text(self,  city: str = "Обухів", lang: str = "ua"):

        data = await WeatherScraper.get_current_weather(city, lang)
        print(data)

        response = self.__client.models.generate_content(
            model=settings.MODEL_AI,
            contents=f"Пристав що ти синоптик і тобі потрібно сформулювати людський опис погоди."
                     f"Наприклад “Сьогодні краще взяти парасольку!”."
                     f"це твої дані на сьогодні {data}."
                     f"2-4 короткі речення не більше"
        )
        print(response.text)


if __name__ == "__main__":
    llm = GeminiLLM()
    asyncio.run(llm.generate())