from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.api.routes_weather import router
from app.db.database import base, engine
from fastapi.staticfiles import StaticFiles
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Перевіряємо структуру бази даних...")
    base.metadata.create_all(bind=engine)
    print("Таблиці створено або вже існують")
    yield
    print("Завершення роботи програми...")

app = FastAPI(title="Weather AI", lifespan=lifespan)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_FILES_DIR = BASE_DIR / "static"
app.mount("/static", StaticFiles(directory=STATIC_FILES_DIR), name="static")

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
