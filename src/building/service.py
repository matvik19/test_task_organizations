from sqlalchemy.ext.asyncio import AsyncSession
from src.building.repository import BuildingRepository
from src.building.schemas import BuildingCreateSchema
from src.common.exceptions import (
    BuildingNotFoundException,
    InvalidBuildingDataException,
    DuplicateBuildingAddressException,
    InvalidCoordinatesException,
    InvalidAddressException,
)
from src.common.exceptions import ItemNotExist


class BuildingService:
    def __init__(self, repository: BuildingRepository):
        self.repository: BuildingRepository = repository

    async def create_building(self, session: AsyncSession, data: BuildingCreateSchema):
        # Валидация данных
        if not data.address or len(data.address.strip()) == 0:
            raise InvalidAddressException("Адрес не может быть пустым")

        # Валидация координат
        if not (-90 <= data.latitude <= 90) or not (-180 <= data.longitude <= 180):
            raise InvalidCoordinatesException()

        # Проверка на дубликат адреса
        existing_building = await self.repository.find_by_address(session, data.address)
        if existing_building:
            raise DuplicateBuildingAddressException(data.address)

        data_dict = data.model_dump()
        return await self.repository.create_one(session, data_dict)

    async def get_building(self, session: AsyncSession, building_id: int):
        try:
            return await self.repository.find_one(session, building_id)
        except ItemNotExist:
            raise BuildingNotFoundException(building_id)

    async def get_buildings(
        self, session: AsyncSession, limit: int = None, offset: int = None
    ):
        return await self.repository.find_all(session, limit, offset)

    async def get_buildings_in_radius(
        self, session: AsyncSession, lat: float, lon: float, radius: float
    ):
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            raise InvalidCoordinatesException()
        if radius <= 0:
            raise InvalidBuildingDataException(
                "Радиус должен быть положительным числом"
            )
        return await self.repository.find_in_radius(session, lat, lon, radius)

    async def get_buildings_in_bbox(
        self,
        session: AsyncSession,
        lat_min: float,
        lat_max: float,
        lon_min: float,
        lon_max: float,
    ):
        if (
            not (-90 <= lat_min <= 90)
            or not (-90 <= lat_max <= 90)
            or not (-180 <= lon_min <= 180)
            or not (-180 <= lon_max <= 180)
        ):
            raise InvalidCoordinatesException()
        if lat_min >= lat_max or lon_min >= lon_max:
            raise InvalidBuildingDataException(
                "Минимальные значения координат должны быть меньше максимальных"
            )
        return await self.repository.find_in_bbox(
            session, lat_min, lat_max, lon_min, lon_max
        )
