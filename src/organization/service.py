from sqlalchemy.ext.asyncio import AsyncSession
from src.organization.repository import OrganizationRepository
from src.organization.schemas import OrganizationCreateSchema, OrganizationUpdateSchema
from src.organization.routers import OrganizationFilterSchema


class OrganizationService:
    def __init__(self, repository: OrganizationRepository):
        self.repository: OrganizationRepository = repository

    async def create_organization(
        self, session: AsyncSession, data: OrganizationCreateSchema
    ):
        data_dict = data.model_dump()
        data_dict["phones"] = [phone.model_dump() for phone in data.phones]
        return await self.repository.create_one(session, data_dict)

    async def get_organization(self, session: AsyncSession, org_id: int):
        return await self.repository.find_one(session, org_id)

    async def get_filtered_organizations(
        self, session: AsyncSession, filters: OrganizationFilterSchema
    ):
        if filters.building_id is not None:
            return await self.repository.find_by_building(
                session, filters.building_id, filters.limit, filters.offset
            )
        if filters.activity_id is not None:
            return await self.repository.find_by_activity_tree(
                session, filters.activity_id, filters.limit, filters.offset
            )
        if filters.search is not None:
            return await self.repository.find_by_name(
                session, filters.search, filters.limit, filters.offset
            )
        if (
            filters.lat is not None
            and filters.lon is not None
            and filters.radius is not None
        ):
            return await self.repository.find_by_radius(
                session,
                filters.lat,
                filters.lon,
                filters.radius,
                filters.limit,
                filters.offset,
            )
        if (
            filters.lat_min is not None
            and filters.lat_max is not None
            and filters.lon_min is not None
            and filters.lon_max is not None
        ):
            return await self.repository.find_by_bbox(
                session,
                filters.lat_min,
                filters.lat_max,
                filters.lon_min,
                filters.lon_max,
                filters.limit,
                filters.offset,
            )
        return await self.repository.find_all(session, filters.limit, filters.offset)
