from src.activity.repository import ActivityRepository
from src.activity.service import ActivityService


def activity_service() -> ActivityService:
    return ActivityService(repository=ActivityRepository())
