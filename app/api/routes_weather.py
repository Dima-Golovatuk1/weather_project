from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.database import session
from app.models.weather import WeatherReport
from app.llm.llm_models import GeminiLLM
from app.scraping.weather_service import WeatherScraper

router = APIRouter()
llm_service = GeminiLLM()
weather_service = WeatherScraper()


def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()


@router.get("/weather/today")
async def get_today_weather(city: str = "Обухів"):
    try:
        data = await weather_service.get_current_weather(city=city)
        ai_text = await llm_service.generate_al_text(city=city)

    except Exception as e:
        print(f"Помилка при обробці запиту: {e}")
        raise HTTPException(status_code=500, detail=f"Помилка при отриманні даних: {e}")

    return {
        "city": data["city"],
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "wind_speed": data["wind_speed"],
        "description": ai_text,
    }


@router.post("/weather/save/today")
async def save_weather_today(city: str = "Обухів"):
    data = await weather_service.get_current_weather(city=city)
    ai_text = await llm_service.generate_al_text(city=city)

    report = WeatherReport(
        city=data["city"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        wind_speed=data["wind_speed"],
        description=ai_text,
    )

    saved_report = report.save()
    return {"message": "Збережено успішно!", "id": saved_report.id}


@router.get("/weather/all")
def get_all_weather(db: Session = Depends(get_db)):
    try:
        reports = db.query(WeatherReport).order_by(WeatherReport.id.desc()).all()
        weather_list = []
        for report in reports:
            weather_list.append({
                "id": report.id,
                "city": report.city,
                "temperature": report.temperature,
                "humidity": report.humidity,
                "wind_speed": report.wind_speed,
                "description": report.description,
                "created_at": report.created_at,
            })
        return weather_list
    except Exception as e:
        print(f"Помилка при отриманні даних з БД: {e}")
        raise HTTPException(status_code=500, detail=f"Помилка при читанні з бази: {e}")

