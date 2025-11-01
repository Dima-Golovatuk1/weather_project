from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
from app.core.config import settings

engine = create_engine(
    url=settings.DATABASE_URL,
    echo=False,
    # pool_size=5,
    # max_overflow=10,
)

session = sessionmaker(bind=engine)
base = declarative_base()


if __name__ == "__main__":
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)