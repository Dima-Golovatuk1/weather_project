import asyncio
from app.core import LLM, settings
from app.scraping.weather_service import WeatherScraper
from google import genai
import google.generativeai as genai

genai.configure(api_key=settings.API_KEY_AI)
weather = WeatherScraper

class GeminiLLM(LLM):

    def __init__(self):
        self.model = genai.GenerativeModel(settings.MODEL_AI)

    async def generate_al_text(self,  city: str = "Обухів", lang: str = "ua"):

        data = await WeatherScraper.get_current_weather(city, lang)

        response = await asyncio.to_thread(
            self.model.generate_content,
            f"Пристав що ти синоптик і тобі потрібно сформулювати людський опис погоди. "
            f"Наприклад: 'Сьогодні краще взяти парасольку!'. "
            f"Ось дані про погоду: {data}. "
            f"Зроби 2–4 короткі речення, не більше. "
            f"Дай лише один варіант відповіді."
        )

        return response.text


# if __name__ == "__main__":
#     llm = GeminiLLM()
#     print(asyncio.run(llm.generate_al_text()))