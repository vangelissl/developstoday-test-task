from fastapi import Depends

from app.repositories.project_repo import ProjectRepository
from app.repositories.place_repo import PlaceRepository

from app.services.project_service import ProjectService
from app.services.place_service import PlaceService


from .database import get_db, AsyncSession


async def get_project_repo(
    session: AsyncSession = Depends(get_db),
) -> ProjectRepository:
    return ProjectRepository(session)


async def get_project_service(
    project_repo: ProjectRepository = Depends(get_project_repo)
) -> ProjectService:
    return ProjectService(project_repo)


async def get_place_repo(
    session: AsyncSession = Depends(get_db),
) -> PlaceRepository:
    return PlaceRepository(session)


async def get_place_service(
    place_repo: PlaceRepository = Depends(get_place_repo),
    project_repo: ProjectRepository = Depends(get_project_repo)
) -> PlaceService:
    return PlaceService(place_repo, project_repo)
