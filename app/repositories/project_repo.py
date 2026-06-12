from ..database import AsyncSession
from ..domain.models import ProjectModel

from sqlalchemy import select
from sqlalchemy.orm import selectinload

import uuid


class ProjectRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: uuid.UUID) -> ProjectModel | None:
        result = await self.session.scalars(
            select(ProjectModel)
            .options(selectinload(ProjectModel.places))
            .where(ProjectModel.id == id)
		)
        return result.first()

    async def get_all(self, limit: int = 50, offset: int = 0) -> list[ProjectModel]:
        projects = (await self.session.scalars(
            select(ProjectModel)
            .options(selectinload(ProjectModel.places))
            .limit(limit)
            .offset(offset)
        )).all()
        
        return list(projects)

    async def create(self, project: ProjectModel) -> ProjectModel:
        self.session.add(project)
        await self.session.flush()
        await self.session.refresh(project)
        return project
    
    async def update(self, id: uuid.UUID, data: dict) -> ProjectModel | None:
        project = await self.session.get(ProjectModel, id)

        if not project:
            return None
            
        for key, value in data.items():
            setattr(project, key, value)
        await self.session.flush()
        await self.session.refresh(project)
        return project
        
    async def delete(self, project: ProjectModel) -> bool:
        await self.session.delete(project)
        await self.session.flush()
        
        return True