from fastapi import APIRouter, Depends, HTTPException, status
from ..domain.schemas import CreatePlace, UpdatePlace, ResponsePlace
from ..dependencies import get_place_service
from ..services.place_service import PlaceService
import uuid

router = APIRouter(prefix="/projects/{project_id}/places", tags=["places"])


@router.post("/", response_model=ResponsePlace, status_code=status.HTTP_201_CREATED)
async def add_place(
    project_id: uuid.UUID,
    body: CreatePlace,
    place_service: PlaceService = Depends(get_place_service),
):
    try:
        return await place_service.add_to_project(project_id, body.external_id)
    except ValueError as e:
        detail = str(e)
        if "not found" in detail:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


@router.get("/", response_model=list[ResponsePlace])
async def get_places(
    project_id: uuid.UUID,
    limit: int = 50,
    offset: int = 0,
    place_service: PlaceService = Depends(get_place_service),
):
    return await place_service.get_all(project_id, limit=limit, offset=offset)


@router.get("/{place_id}", response_model=ResponsePlace)
async def get_place(
    project_id: uuid.UUID,
    place_id: uuid.UUID,
    place_service: PlaceService = Depends(get_place_service),
):
    try:
        return await place_service.get(place_id, project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{place_id}", response_model=ResponsePlace)
async def update_place(
    project_id: uuid.UUID,
    place_id: uuid.UUID,
    body: UpdatePlace,
    place_service: PlaceService = Depends(get_place_service),
):
    try:
        data = body.model_dump(exclude_none=True)
        return await place_service.update(place_id, project_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))