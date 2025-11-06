from sqlalchemy import Column, Integer, String, Float, Date
from app.db.database import async_session, Base
from sqlalchemy.future import select

class WeatherReport(Base):
    __tablename__ = "weather_reports"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    description = Column(String)
    reported_at = Column(Date)

    async def save(self):
        async with async_session() as db:
            async with db.begin():
                db.add(self)
            await db.refresh(self)
            return self

    @classmethod
    async def get_by_id(cls, report_id: int):
        async with async_session() as db:
            result = await db.execute(select(cls).filter(cls.id == report_id))
            return result.scalar_one_or_none()

    @classmethod
    async def delete_by_id(cls, report_id: int):
        async with async_session() as db:
            result = await db.execute(select(cls).filter(cls.id == report_id))
            report = result.scalar_one_or_none()
            if not report:
                return None
            await db.delete(report)
            await db.commit()
            return True
