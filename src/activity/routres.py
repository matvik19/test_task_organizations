from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.activity.schemas import ActivityResponseSchema, ActivityCreateSchema
from src.activity.service import ActivityService
from src.activity.dependencies import activity_service
from src.common.database import get_async_session
from src.common.verify_key import verify_api_key
from src.common.logger import logger
from src.common.exceptions import (
    ActivityNotFoundException,
    InvalidActivityDataException,
    DuplicateActivityNameException,
    ParentActivityNotFoundException,
    CircularDependencyException,
)

activity_router = APIRouter(
    prefix="/activities",
    tags=["activities"],
    dependencies=[Depends(verify_api_key)],
)


@activity_router.get(
    "",
    response_model=list[ActivityResponseSchema],
    description="Получить список всех видов деятельности с пагинацией",
)
async def get_activities(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: ActivityService = Depends(activity_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.get_activities(session, limit, offset)
    except Exception as e:
        logger.error(f"Ошибка при получении списка видов деятельности: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении списка видов деятельности",
        )


@activity_router.get(
    "/{activity_id}",
    response_model=ActivityResponseSchema,
    description="Получить подробную информацию о виде деятельности по его идентификатору",
)
async def get_activity(
    activity_id: int,
    service: ActivityService = Depends(activity_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.get_activity(session, activity_id)
    except ActivityNotFoundException as e:
        raise
    except Exception as e:
        logger.error(
            f"Ошибка при получении информации о виде деятельности {activity_id}: {str(e)}"
        )
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при получении информации о виде деятельности",
        )


@activity_router.post(
    "",
    response_model=ActivityResponseSchema,
    description="Создать новый вид деятельности с возможной вложенностью",
)
async def create_activity(
    data: ActivityCreateSchema,
    service: ActivityService = Depends(activity_service),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        return await service.create_activity(session, data)
    except (
        InvalidActivityDataException,
        DuplicateActivityNameException,
        ParentActivityNotFoundException,
        CircularDependencyException,
    ) as e:
        raise
    except Exception as e:
        logger.error(f"Ошибка при создании вида деятельности: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера при создании вида деятельности",
        )
