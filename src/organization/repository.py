from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.activity.models import OrganizationActivity, Activity
from src.common.repository import SQLAlchemyRepository
from src.organization.models import Organization, OrganizationPhone
from src.organization.schemas import OrganizationCreateSchema
from src.building.models import Building


class OrganizationRepository(SQLAlchemyRepository):
    model = Organization

    async def find_one(self, session: AsyncSession, id: int):
        stmt = (
            select(self.model)
            .where(self.model.id == id)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
        )
        res = await session.execute(stmt)
        return res.scalar_one()

    async def find_all(self, session: AsyncSession, limit: int = 10, offset: int = 0):
        stmt = (
            select(self.model)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
            .limit(limit)
            .offset(offset)
        )
        res = await session.execute(stmt)
        return res.scalars().all()

    async def find_by_building(
        self, session: AsyncSession, building_id: int, limit: int = 10, offset: int = 0
    ):
        stmt = (
            select(self.model)
            .where(self.model.building_id == building_id)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
            .limit(limit)
            .offset(offset)
        )
        return (await session.execute(stmt)).scalars().all()

    async def find_by_activity(self, session: AsyncSession, activity_id: int):
        """Поиск организаций по деятельности"""
        stmt = (
            select(self.model)
            .join(OrganizationActivity)
            .where(OrganizationActivity.activity_id == activity_id)
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
        )
        return (await session.execute(stmt)).scalars().all()

    async def find_by_radius(
        self,
        session: AsyncSession,
        lat: float,
        lon: float,
        radius: float,
        limit: int = 10,
        offset: int = 0,
    ):
        stmt = (
            select(self.model)
            .join(Building, self.model.building_id == Building.id)
            .where(
                and_(
                    Building.latitude >= lat - radius,
                    Building.latitude <= lat + radius,
                    Building.longitude >= lon - radius,
                    Building.longitude <= lon + radius,
                )
            )
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
            .limit(limit)
            .offset(offset)
        )
        return (await session.execute(stmt)).scalars().all()

    async def find_by_name(
        self, session: AsyncSession, name: str, limit: int = 10, offset: int = 0
    ):
        stmt = (
            select(self.model)
            .where(self.model.name.ilike(f"%{name}%"))
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
            .limit(limit)
            .offset(offset)
        )
        return (await session.execute(stmt)).scalars().all()

    async def find_by_activity_tree(
        self, session: AsyncSession, activity_id: int, limit: int = 10, offset: int = 0
    ):
        cte = select(Activity.id).where(Activity.id == activity_id).cte(recursive=True)
        cte = cte.union_all(
            select(Activity.id).join(cte, Activity.parent_id == cte.c.id)
        )
        stmt = (
            select(self.model)
            .join(OrganizationActivity)
            .where(OrganizationActivity.activity_id.in_(select(cte.c.id)))
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
            .limit(limit)
            .offset(offset)
        )
        return (await session.execute(stmt)).scalars().all()

    async def find_by_bbox(
        self,
        session: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
        limit: int = 10,
        offset: int = 0,
    ):
        stmt = (
            select(self.model)
            .join(Building, self.model.building_id == Building.id)
            .where(
                and_(
                    Building.latitude >= lat_min,
                    Building.latitude <= lat_max,
                    Building.longitude >= lon_min,
                    Building.longitude <= lon_max,
                )
            )
            .options(
                selectinload(self.model.building),
                selectinload(self.model.activities),
                selectinload(self.model.phones),
            )
            .limit(limit)
            .offset(offset)
        )
        return (await session.execute(stmt)).scalars().all()
