from ..repositories.place_repo import PlaceRepository
from ..repositories.project_repo import ProjectRepository
from ..domain.models import PlaceModel
from ..services.aic_client import fetch_artwork, parse_artwork
import uuid

MAX_PLACES = 10


class PlaceService:
    def __init__(self, place_repo: PlaceRepository, project_repo: ProjectRepository):
        self.place_repo = place_repo
        self.project_repo = project_repo

    async def get(self, place_id: uuid.UUID, project_id: uuid.UUID) -> PlaceModel:
        place = await self.place_repo.get(place_id, project_id)
        if not place:
            raise ValueError(f"Place {place_id} not found in project {project_id}")
        return place

    async def get_all(self, project_id: uuid.UUID, limit: int = 50, offset: int = 0) -> list[PlaceModel]:
        return await self.place_repo.get_all(project_id, limit, offset)

    async def add_to_project(self, project_id: uuid.UUID, external_id: int) -> PlaceModel:
        # enforce max places
        count = await self.place_repo.count_for_project(project_id)
        if count >= MAX_PLACES:
            raise ValueError(f"Project cannot have more than {MAX_PLACES} places")

        # prevent duplicates
        existing = await self.place_repo.get_by_external_id(project_id, external_id)
        if existing:
            raise ValueError(f"Place {external_id} already exists in this project")

        # validate + fetch from AIC
        data = await fetch_artwork(external_id)
        parsed = parse_artwork(data)

        place = PlaceModel(
            id=uuid.uuid4(),
            project_id=project_id,
            external_id=external_id,
            title=parsed["title"],
            artist=parsed["artist"],
            image_url=parsed["image_url"],
            is_visited=False,
        )
        return await self.place_repo.create(place)

    async def update(self, place_id: uuid.UUID, project_id: uuid.UUID, data: dict) -> PlaceModel:
        updated = await self.place_repo.update(place_id, project_id, data)
        if not updated:
            raise ValueError(f"Place {place_id} not found in project {project_id}")

        # auto-complete project if all places visited
        if updated.is_visited:
            all_places = await self.place_repo.get_all(project_id)
            if all(p.is_visited for p in all_places):
                await self.project_repo.update(project_id, {"is_completed": True})

        return updated