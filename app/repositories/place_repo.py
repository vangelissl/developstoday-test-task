from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..domain.models import PlaceModel
import uuid


class PlaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, place_id: uuid.UUID, project_id: uuid.UUID) -> PlaceModel | None:
        result = await self.session.scalars(
            select(PlaceModel)
            .where(PlaceModel.id == place_id)
            .where(PlaceModel.project_id == project_id)
        )
        return result.first()

    async def get_all(self, project_id: uuid.UUID, limit: int = 50, offset: int = 0) -> list[PlaceModel]:
        result = await self.session.scalars(
            select(PlaceModel)
            .where(PlaceModel.project_id == project_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.all())

    async def get_by_external_id(self, project_id: uuid.UUID, external_id: int) -> PlaceModel | None:
        result = await self.session.scalars(
            select(PlaceModel)
            .where(PlaceModel.project_id == project_id)
            .where(PlaceModel.external_id == external_id)
        )
        return result.first()

    async def count_for_project(self, project_id: uuid.UUID) -> int:
        result = await self.session.scalars(
            select(PlaceModel)
            .where(PlaceModel.project_id == project_id)
        )
        return len(result.all())

    async def create(self, place: PlaceModel) -> PlaceModel:
        self.session.add(place)
        await self.session.flush()
        await self.session.refresh(place)
        return place

    async def update(self, place_id: uuid.UUID, project_id: uuid.UUID, data: dict) -> PlaceModel | None:
        place = await self.get(place_id, project_id)
        if not place:
            return None
        for key, value in data.items():
            setattr(place, key, value)
        await self.session.flush()
        await self.session.refresh(place)
        return place
