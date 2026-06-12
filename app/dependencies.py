from fastapi import Depends

from app.repositories.project_repo import ProjectRepository
from app.services.project_service import ProjectService
from .database import get_db, AsyncSession


async def get_project_repo(
		session: AsyncSession = Depends(get_db), 
) -> ProjectRepository:
	return ProjectRepository(session)


async def get_project_service(
		project_repo: ProjectRepository = Depends(get_project_repo)
) -> ProjectService:
	return ProjectService(project_repo)