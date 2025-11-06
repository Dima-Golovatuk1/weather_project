from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from pathlib import Path


env_path = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    API_KEY_AI: str
    MODEL_AI: str
    API_KEY_WEATHER: str
    HOST: str
    DATABASE: str
    USER: str
    PASSWORD: str
    DATABASE_PORT: int
    LLM_MODEL: str = "gemini-2.5-flash"

    model_config = ConfigDict(env_file=str(env_path))

    # @property
    # def DATABASE_URL(self):
    #     return (
    #         f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}"
    #         f"@{self.HOST}:{self.DATABASE_PORT}/{self.DATABASE}"
    #     )

    @property
    def DATABASE_URL(self):
        return (
            f"postgresql+psycopg://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.DATABASE_PORT}/{self.DATABASE}"
        )


settings = Settings()

if __name__ == "__main__":
    print("Використовується .env:", env_path)
    print("DATABASE_URL:", settings.DATABASE_URL)
    print("WEATHER_URL:", settings.API_KEY_WEATHER)
