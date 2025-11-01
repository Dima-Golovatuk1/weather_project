from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.database import base

class WeatherReport(base):
    __tablename__ = "weather_reports"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
