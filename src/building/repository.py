from sqlalchemy import select, insert, and_
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.repository import SQLAlchemyRepository
from src.building.models import Building


class BuildingRepository(SQLAlchemyRepository[Building]):
    model = Building

    async def find_one(self, session: AsyncSession, id: int):
        stmt = select(self.model).where(self.model.id == id)
        res = await session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, session: AsyncSession, limit: int = None, offset: int = None):
        stmt = select(self.model)
        if limit is not None:
            stmt = stmt.limit(limit)
        if offset is not None:
            stmt = stmt.offset(offset)
        res = await session.execute(stmt)
        return res.scalars().all()

    async def find_by_address(self, session: AsyncSession, address: str):
        stmt = select(self.model).where(self.model.address == address)
        res = await session.execute(stmt)
        return res.scalar_one_or_none()

    async def find_in_radius(self, session: AsyncSession, lat: float, lon: float, radius: float):
        stmt = select(self.model).where(
            and_(
                self.model.latitude >= lat - radius,
                self.model.latitude <= lat + radius,
                self.model.longitude >= lon - radius,
                self.model.longitude <= lon + radius,
            )
        )
        res = await session.execute(stmt)
        return res.scalars().all()

    async def find_in_bbox(
        self,
        session: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ):
        stmt = select(self.model).where(
            and_(
                self.model.latitude >= lat_min,
                self.model.latitude <= lat_max,
                self.model.longitude >= lon_min,
                self.model.longitude <= lon_max,
            )
        )
        res = await session.execute(stmt)
        return res.scalars().all()

    async def create_one(self, session: AsyncSession, data: dict) -> Building:
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalar_one()
