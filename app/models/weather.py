from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from datetime import datetime, timezone
from app.db.database import base, session


class WeatherReport(base):
    __tablename__ = "weather_reports"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String)
    reported_at = Column(Date)

    def save(self):
        db = session()
        try:
            db.add(self)
            db.commit()
            db.refresh(self)
            return self
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

