from fastapi import APIRouter, Depends, HTTPException, status
from ..domain.schemas import CreateProject, UpdateProject, ResponseProject, ResponseProjectDetail
from ..domain.models import ProjectModel
from ..dependencies import get_project_service
from ..services.project_service import ProjectService
import uuid

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ResponseProject, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: CreateProject,
    project_service: ProjectService = Depends(get_project_service),
):
    project = ProjectModel(
        name=body.name,
        description=body.description,
        start_date=body.start_date,
    )
    return await project_service.create(project, place_ids=body.places)


@router.get("/", response_model=list[ResponseProject])
async def get_projects(
    limit: int = 50,
    offset: int = 0,
    is_completed: bool | None = None,
    project_service: ProjectService = Depends(get_project_service),
):
    return await project_service.get_all(limit=limit, offset=offset, is_completed=is_completed)


@router.get("/{project_id}", response_model=ResponseProjectDetail)
async def get_project(
    project_id: uuid.UUID,
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        return await project_service.get(project_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.patch("/{project_id}", response_model=ResponseProject)
async def update_project(
    project_id: uuid.UUID,
    body: UpdateProject,
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        data = body.model_dump(exclude_none=True)
        return await project_service.update(project_id, data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: uuid.UUID,
    project_service: ProjectService = Depends(get_project_service),
):
    try:
        await project_service.delete(project_id)
    except ValueError as e:
        detail = str(e)
        status_code = status.HTTP_400_BAD_REQUEST if "visited" in detail else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=detail)