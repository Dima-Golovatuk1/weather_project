from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.api.routes_weather import router
from app.db.database import base, engine
from app.models import weather


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Перевіряємо структуру бази даних...")
    base.metadata.create_all(bind=engine)
    print("Таблиці створено або вже існують")
    yield
    print("Завершення роботи програми...")


app = FastAPI(title="Weather AI", lifespan=lifespan)
app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
