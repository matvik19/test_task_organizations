from src.organization.repository import OrganizationRepository
from src.organization.service import OrganizationService


def organization_service() -> OrganizationService:
    return OrganizationService(repository=OrganizationRepository())