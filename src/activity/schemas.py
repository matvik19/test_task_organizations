from src.common.schema import BaseSchema
from pydantic import model_validator


class ActivityCreateSchema(BaseSchema):
    name: str
    parent_id: int | None = None


class ActivityResponseSchema(BaseSchema):
    id: int
    name: str
    parent_id: int | None
    children_ids: list[int]

    @model_validator(mode="before")
    @classmethod
    def extract_children(cls, data: any) -> any:
        if hasattr(data, "children"):
            data.children_ids = [child.id for child in data.children]
        return data
