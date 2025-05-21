import asyncio
import subprocess
from loguru import logger
from typing import AsyncGenerator

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.common.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


class Base(DeclarativeBase):
    pass


engine = create_async_engine(
    DATABASE_URL,
    pool_size=30,
    max_overflow=25,
    echo=False,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def wait_for_db():
    """Ожидаем доступности базы данных перед запуском сервиса"""
    retries = 10
    while retries:
        try:
            conn = await asyncpg.connect(
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
                host=DB_HOST,
                port=DB_PORT,
            )
            await conn.close()
            logger.info("База данных готова к работе.")
            return
        except Exception as e:
            logger.warning(
                f"База данных не готова, повторная попытка... Осталось попыток: {retries}. Ошибка: {e}"
            )
            retries -= 1
            await asyncio.sleep(2)
    logger.error("База данных недоступна, завершение работы.")
    exit(1)


async def run_migrations():
    """Запускаем Alembic миграции"""
    logger.info("Запуск миграций базы данных...")
    subprocess.run("alembic upgrade head", shell=True, check=True)
    logger.info("Миграции успешно выполнены.")
