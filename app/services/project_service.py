from app.domain.models import ProjectModel

from ..repositories.project_repo import ProjectRepository

import uuid


class ProjectService:
	def __init__(self, project_repo: ProjectRepository):
		self.project_repo = project_repo

	async def get(self, id: uuid.UUID) -> ProjectModel:
		project = await self.project_repo.get(id)
		if not project:
			raise ValueError(f"Project {id} not found")
		return project

	async def get_all(self, limit: int = 50, offset: int = 0, is_completed: bool | None = None) -> list[ProjectModel]:
		return await self.project_repo.get_all(limit, offset)
	
	async def create(self, project: ProjectModel, place_ids: list[int] = []) -> ProjectModel:
		if not place_ids:
			raise ValueError("Project must have at least 1 place")
		created = await self.project_repo.create(project)
		return created

	async def update(self, id:uuid.UUID, data: dict) -> ProjectModel:
		updated =  await self.project_repo.update(id, data)
		if not updated:
			raise ValueError(f"Project {id} not found")
		return updated

	async def delete(self, id: uuid.UUID) -> bool:
		project = await self.project_repo.get(id)
		if not project:
			raise ValueError(f"Project {id} not found")
		if any(p.is_visited for p in project.places):
			raise ValueError(f"Cannot delete project {id} with visited places")
		result = await self.project_repo.delete(project)
		return result