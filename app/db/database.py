# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker, declarative_base, DeclarativeBase
# from app.core import settings
#
# engine = create_engine(
#     url=settings.DATABASE_URL,
#     echo=False,
#     # pool_size=5,
#     # max_overflow=10,
# )
#
# session = sessionmaker(bind=engine)
# base = declarative_base()
#
#
# if __name__ == "__main__":
#     try:
#         with engine.connect() as connection:
#             result = connection.execute(text("SELECT 1"))
#             print("Database connection successful!", result.scalar())
#     except Exception as e:
#         print("Database connection failed:", e)


import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from app.core import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

Base = declarative_base()

async def test_connection():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!", result.scalar())
    except Exception as e:
        print("Database connection failed:", e)


if __name__ == "__main__":
    if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    asyncio.run(test_connection())

