from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.building.schemas import BuildingResponseSchema, BuildingCreateSchema
from src.building.service import BuildingService
from src.building.dependencies import building_service
from src.common.database import get_async_session
from src.common.verify_key import verify_api_key
from src.common.logger import logger
from src.common.exceptions import (
    BuildingNotFoundException,
    InvalidBuildingDataException,
    DuplicateBuildingAddressException,
    InvalidCoordinatesException,
    InvalidAddressException,
)

building_router = APIRouter(
    prefix="/buildings",
    tags=["buildings"],
    dependencies=[Depends(verify_api_key)],
)


@building_router.get(
    "",
    response_model=list[BuildingResponseSchema],
    description="Получить список всех зданий с пагинацией",
)
async def get_buildings(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: BuildingService = Depends(building_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.get_buildings(session, limit, offset)
    except Exception as e:
        logger.error(f"Ошибка при получении списка зданий: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении списка зданий",
        )


@building_router.get(
    "/{building_id}",
    response_model=BuildingResponseSchema,
    description="Получить подробную информацию о здании по его идентификатору",
)
async def get_building(
    building_id: int,
    service: BuildingService = Depends(building_service),
    session: AsyncSession = Depends(get_async_session),
    api_key: str = Depends(verify_api_key),
):
    try:
        return await service.get_building(session, building_id)
    except BuildingNotFoundException as e:
        raise
    except Exception as e:
        logger.error(
            f"Ошибка при получении информации о здании {building_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении информации о здании",
        )


@building_router.post(
    "",
    response_model=BuildingResponseSchema,
    description="Создать новое здание с адресом и координатами",
)
async def create_building(
    data: BuildingCreateSchema,
    service: BuildingService = Depends(building_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.create_building(session, data)
    except (
        InvalidBuildingDataException,
        DuplicateBuildingAddressException,
        InvalidCoordinatesException,
        InvalidAddressException,
    ) as e:
        raise
    except Exception as e:
        logger.error(f"Ошибка при создании здания: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера при создании здания"
        )
