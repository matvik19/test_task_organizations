from src.common.schema import BaseSchema
from pydantic import Field


class BuildingCreateSchema(BaseSchema):
    address: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class BuildingResponseSchema(BaseSchema):
    id: int
    address: str
    latitude: float
    longitude: float
