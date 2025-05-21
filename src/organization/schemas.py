from dataclasses import dataclass
from typing import Annotated

from fastapi import Query

from src.common.schema import BaseSchema
from pydantic import field_validator, model_validator, Field

from src.organization.models import OrganizationPhone


@dataclass
class OrganizationFilterSchema:
    building_id: Annotated[
        int | None, Query(description="Фильтр по идентификатору здания")
    ] = None
    activity_id: Annotated[
        int | None,
        Query(
            description="Фильтр по идентификатору деятельности (включает подкатегории)"
        ),
    ] = None
    search: Annotated[
        str | None,
        Query(description="Поиск по названию организации (частичное совпадение)"),
    ] = None
    lat: Annotated[
        float | None, Query(ge=-90, le=90, description="Широта для фильтра по радиусу")
    ] = None
    lon: Annotated[
        float | None,
        Query(ge=-180, le=180, description="Долгота для фильтра по радиусу"),
    ] = None
    radius: Annotated[
        float | None,
        Query(gt=0, description="Радиус в градусах для географического фильтра"),
    ] = None
    lat_min: Annotated[
        float | None,
        Query(
            ge=-90, le=90, description="Минимальная широта для прямоугольного фильтра"
        ),
    ] = None
    lat_max: Annotated[
        float | None,
        Query(
            ge=-90, le=90, description="Максимальная широта для прямоугольного фильтра"
        ),
    ] = None
    lon_min: Annotated[
        float | None,
        Query(
            ge=-180,
            le=180,
            description="Минимальная долгота для прямоугольного фильтра",
        ),
    ] = None
    lon_max: Annotated[
        float | None,
        Query(
            ge=-180,
            le=180,
            description="Максимальная долгота для прямоугольного фильтра",
        ),
    ] = None
    limit: Annotated[
        int, Query(ge=1, le=100, description="Количество записей для возврата")
    ] = 10
    offset: Annotated[
        int, Query(ge=0, description="Количество записей для пропуска")
    ] = 0


class OrganizationPhoneSchema(BaseSchema):
    phone: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        """Проверяет, что номер телефона соответствует формату, например 2-222-222 или 8-923-666-13-13"""
        parts = value.split("-")
        if len(parts) not in (3, 5):
            raise ValueError(
                "Номер телефона должен быть в формате X-XXX-XXX или X-XXX-XXX-XX-XX"
            )

        if not (1 <= len(parts[0]) <= 3 and parts[0].isdigit()):
            raise ValueError("Первая часть номера должна содержать 1-3 цифры")

        for part in parts[1:3]:
            if len(part) != 3 or not part.isdigit():
                raise ValueError(
                    "Вторая и третья части номера должны содержать ровно 3 цифры"
                )

        if len(parts) == 5:
            for part in parts[3:5]:
                if len(part) != 2 or not part.isdigit():
                    raise ValueError(
                        "Последние две части номера должны содержать ровно 2 цифры"
                    )

        return value


class OrganizationCreateSchema(BaseSchema):
    name: str
    phones: list[OrganizationPhoneSchema]
    building_id: int
    activity_ids: list[int]


class OrganizationResponseSchema(BaseSchema):
    id: int
    name: str
    phones: list[OrganizationPhoneSchema]
    building_id: int
    building_address: str
    activity_ids: list[int]
    activity_names: list[str]

    @model_validator(mode="before")
    @classmethod
    def extract_related_data(cls, data: any) -> dict:
        result = {}
        if hasattr(data, "building"):
            result["building_id"] = data.building.id
            result["building_address"] = data.building.address
        if hasattr(data, "activities"):
            result["activity_ids"] = [activity.id for activity in data.activities]
            result["activity_names"] = [activity.name for activity in data.activities]
        if hasattr(data, "phones"):
            result["phones"] = [
                OrganizationPhoneSchema(phone=phone.phone)
                for phone in data.phones
                if isinstance(phone, OrganizationPhone) and hasattr(phone, "phone")
            ]
        result.update(data.__dict__)
        return result


class OrganizationUpdateSchema(BaseSchema):
    name: str | None = None
    phones: list[OrganizationPhoneSchema] | None = None
    building_id: int | None = None
    activity_ids: list[int] | None = None
