from src.activity.routres import activity_router
from src.organization.routers import organization_router
from src.building.routers import building_router

all_routers = [
    organization_router,
    activity_router,
    building_router,
]
