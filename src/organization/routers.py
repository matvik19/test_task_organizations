from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.verify_key import verify_api_key
from src.common.logger import logger
from src.organization.schemas import (
    OrganizationResponseSchema,
    OrganizationCreateSchema,
    OrganizationFilterSchema,
)
from src.organization.service import OrganizationService
from src.organization.dependencies import organization_service
from src.common.exceptions import (
    OrganizationNotFoundException,
    BuildingNotFoundException,
    ActivityNotFoundException,
    InvalidCoordinatesException,
    InvalidRadiusException,
    InvalidBoundingBoxException,
    DuplicateOrganizationNameException,
    InvalidPhoneNumberException,
)
from src.common.database import get_async_session


organization_router = APIRouter(
    prefix="/organizations",
    tags=["organizations"],
    dependencies=[Depends(verify_api_key)],
)


@organization_router.get(
    "",
    response_model=list[OrganizationResponseSchema],
    description="Получить список организаций с фильтрами по зданию, деятельности, названию или географии",
)
async def get_organizations(
    filters: Annotated[OrganizationFilterSchema, Depends()],
    service: OrganizationService = Depends(organization_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.get_filtered_organizations(session, filters)
    except (
        InvalidCoordinatesException,
        InvalidRadiusException,
        InvalidBoundingBoxException,
    ) as e:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении списка организаций: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении списка организаций",
        )


@organization_router.post(
    "",
    response_model=OrganizationResponseSchema,
    description="Создать новую организацию",
)
async def create_organization(
    data: OrganizationCreateSchema,
    service: OrganizationService = Depends(organization_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.create_organization(session, data)
    except (
        BuildingNotFoundException,
        ActivityNotFoundException,
        DuplicateOrganizationNameException,
        InvalidPhoneNumberException,
    ) as e:
        raise
    except Exception as e:
        logger.error(f"Ошибка при создании организации: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Внутренняя ошибка сервера при создании организации"
        )


@organization_router.get(
    "/{org_id}",
    response_model=OrganizationResponseSchema,
    description="Получить подробную информацию об организации по её идентификатору",
)
async def get_organization(
    org_id: int,
    service: OrganizationService = Depends(organization_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.get_organization(session, org_id)
    except OrganizationNotFoundException as e:
        raise
    except Exception as e:
        logger.error(
            f"Ошибка при получении информации об организации {org_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении информации об организации",
        )
