from fastapi import APIRouter, HTTPException, Depends, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from app.db.database import session
from app.models.weather import WeatherReport
from app.llm.llm_models import GeminiLLM
from app.scraping.weather_service import WeatherScraper


router = APIRouter()
llm_service = GeminiLLM()
weather_service = WeatherScraper()

BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = BASE_DIR / "templates"
templates = Jinja2Templates(directory=TEMPLATE_DIR)


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# weather_today
@router.get("/weather/today", response_class=HTMLResponse)
async def weather_today_form(request: Request, error: str = None, weather_data: dict = None):
    return templates.TemplateResponse(
        "weather_today.html",
        {"request": request, "error": error, "weather": weather_data}
    )


@router.post("/weather/today", response_class=HTMLResponse)
async def post_today_weather(request: Request, city: str = Form(...)):
    try:
        data = await weather_service.get_current_weather(city=city)
        ai_text = await llm_service.generate_al_text(city=city)

        weather_data = {
            "city": data["city"],
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "wind_speed": data["wind_speed"],
            "description": ai_text,
        }

        return templates.TemplateResponse(
            "weather_today.html",
            {"request": request, "error": None, "weather": weather_data}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "weather_today.html",
            {"request": request, "error": f"Не вдалося отримати дані"}
        )


# weather_save
@router.get("/weather/save", response_class=HTMLResponse)
async def weather_save_form(request: Request, message: str = None, error: str = None):
    return templates.TemplateResponse(
        "weather_save_today.html",
        {"request": request, "message": message, "error": error}
    )


@router.post("/weather/save", response_class=HTMLResponse)
async def save_weather_report(request: Request, city: str = Form(...)):
    try:
        data = await weather_service.get_current_weather(city=city)
        ai_text = await llm_service.generate_al_text(city=city)

        report = WeatherReport(
            city=data["city"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            wind_speed=data["wind_speed"],
            description=ai_text,
            reported_at=data["reported_at"]
        )
        report.save()
        message = f"Погода для {city} успішно збережена в базу даних!"

        return templates.TemplateResponse(
            "weather_save_today.html",
            {
                "request": request,
                "message": message,
                "error": None
            }
        )
    except Exception as e:
        return templates.TemplateResponse(
            "weather_save_today.html",
            {"request": request, "error": f"Винекла помилка"}
        )



# get_weather_all
@router.get("/weather/history", response_class=HTMLResponse)
def get_all_weather(request: Request, db: Session = Depends(get_db)):
    try:
        reports = db.query(WeatherReport).order_by(WeatherReport.id.desc()).all()
        return templates.TemplateResponse(
            "weather_all.html",
            {"request": request, "reports": reports}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "all.html",
            {"request": request, "error": f"Помилка при читанні з бази: {e}"}
        )

