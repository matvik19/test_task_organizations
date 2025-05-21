from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.common.repository import SQLAlchemyRepository
from src.activity.models import Activity


class ActivityRepository(SQLAlchemyRepository[Activity]):
    model = Activity

    async def find_one(self, session: AsyncSession, id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.parent),
                selectinload(self.model.children),
                selectinload(self.model.organizations),
            )
        )
        res = await session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, session: AsyncSession, limit: int = None, offset: int = None):
        stmt = select(self.model).options(
            selectinload(self.model.parent),
            selectinload(self.model.children),
            selectinload(self.model.organizations),
        )
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await session.execute(stmt)
        return res.scalars().all()

    async def find_by_name(self, session: AsyncSession, name: str):
        stmt = (
            select(self.model)
            .where(self.model.name == name)
            .options(
                selectinload(self.model.parent),
                selectinload(self.model.children),
                selectinload(self.model.organizations),
            )
        )
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def create_one(self, session: AsyncSession, data: dict) -> Activity:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()
