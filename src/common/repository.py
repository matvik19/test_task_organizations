from abc import ABC, abstractmethod
from typing import Generic, Protocol, TypeVar, Optional, List
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from src.common.exceptions import ItemNotExist


class HasId(Protocol):
    id: Mapped[int]


T = TypeVar("T", bound=HasId)


class AbstractRepository(ABC, Generic[T]):
    """Абстрактный базовый класс для репозиториев"""

    @abstractmethod
    async def create_one(self, session: AsyncSession, data: dict) -> T:
        """Создание одной записи"""
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, session: AsyncSession, id: int) -> T:
        """Поиск одной записи по id"""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, session: AsyncSession) -> List[T]:
        """Получение всех записей"""
        raise NotImplementedError

    @abstractmethod
    async def update_one(
        self, session: AsyncSession, id: int, data: dict
    ) -> Optional[T]:
        """Обновление одной записи"""
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, session: AsyncSession, id: int) -> None:
        """Удаление одной записи"""
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[T]):
    """Базовый класс для SQLAlchemy репозиториев"""

    model: type[T]

    async def create_one(self, session: AsyncSession, data: dict) -> T:
        """Создание одной записи"""
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()

    async def find_one(self, session: AsyncSession, id: int):
        """Поиск одной записи по id"""
        stmt = select(self.model).where(self.model.id == id)
        res = await session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, session: AsyncSession):
        """Получение всех записей"""
        stmt = select(self.model)
        res = await session.execute(stmt)
        return res.scalars().all()

    async def update_one(self, session: AsyncSession, id: int, data: dict):
        """Обновление одной записи"""
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**data)
            .returning(self.model)
        )
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one_or_none()

    async def delete_one(self, session: AsyncSession, id: int):
        """Удаление одной записи"""
        stmt = delete(self.model).where(self.model.id == id)
        res = await session.execute(stmt)
        await session.commit()
        if res.rowcount == 0:
            raise ItemNotExist

    async def update_all(self, session: AsyncSession, data: dict):
        """Обновление всех записей"""
        stmt = update(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalars().all()

    async def find_one_or_none(self, session: AsyncSession, item_id: int):
        """Поиск одной записи по id или None если не найдено"""
        stmt = select(self.model).where(self.model.id == item_id)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()
