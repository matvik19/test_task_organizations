from src.building.repository import BuildingRepository
from src.building.service import BuildingService


def building_service() -> BuildingService:
    return BuildingService(repository=BuildingRepository())
