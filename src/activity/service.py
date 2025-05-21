from sqlalchemy.ext.asyncio import AsyncSession
from src.activity.repository import ActivityRepository
from src.activity.schemas import ActivityCreateSchema
from src.common.exceptions import (
    ActivityNotFoundException,
    InvalidActivityDataException,
    DuplicateActivityNameException,
    ParentActivityNotFoundException,
    CircularDependencyException,
)
from src.common.exceptions import ItemNotExist


class ActivityService:
    def __init__(self, repository: ActivityRepository):
        self.repository: ActivityRepository = repository

    async def create_activity(self, session: AsyncSession, data: ActivityCreateSchema):
        # Валидация данных
        if not data.name or len(data.name.strip()) == 0:
            raise InvalidActivityDataException("Название не может быть пустым")

        # Проверка на дубликат
        existing_activity = await self.repository.find_by_name(session, data.name)
        if existing_activity:
            raise DuplicateActivityNameException(data.name)

        # Если указан родительский вид деятельности, проверяем его существование
        if data.parent_id is not None:
            try:
                parent = await self.repository.find_one(session, data.parent_id)
                if not parent:
                    raise ParentActivityNotFoundException(data.parent_id)

                # Проверка на циклическую зависимость
                if await self._check_circular_dependency(
                    session, data.parent_id, data.name
                ):
                    raise CircularDependencyException()
            except ItemNotExist:
                raise ParentActivityNotFoundException(data.parent_id)

        data_dict = data.model_dump()
        return await self.repository.create_one(session, data_dict)

    async def get_activity(self, session: AsyncSession, activity_id: int):
        try:
            return await self.repository.find_one(session, activity_id)
        except ItemNotExist:
            raise ActivityNotFoundException(activity_id)

    async def get_activities(self, session: AsyncSession, limit: int = None, offset: int = None):
        return await self.repository.find_all(session, limit, offset)

    async def _check_circular_dependency(
        self, session: AsyncSession, parent_id: int, new_name: str
    ) -> bool:
        """
        Проверяет, не создаст ли добавление нового вида деятельности циклическую зависимость
        """
        current_id = parent_id
        visited = set()

        while current_id is not None:
            if current_id in visited:
                return True
            visited.add(current_id)

            try:
                activity = await self.repository.find_one(session, current_id)
                if not activity:
                    return False
                current_id = activity.parent_id
            except ItemNotExist:
                return False

        return False
