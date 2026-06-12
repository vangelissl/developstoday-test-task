from pydantic import BaseModel, ConfigDict
from datetime import datetime
import uuid


class CreateProject(BaseModel):
    name: str
    description: str | None = None
    start_date: datetime | None = None
    places: list[int] = []  


class UpdateProject(BaseModel):
    name: str | None = None
    description: str | None = None
    start_date: datetime | None = None


class ResponseProject(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    description: str | None
    start_date: datetime | None
    is_completed: bool



class CreatePlace(BaseModel):
    external_id: int  


class UpdatePlace(BaseModel):
    notes: str | None = None
    is_visited: bool | None = None


class ResponsePlace(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    external_id: int
    title: str
    artist: str | None
    image_url: str | None
    notes: str | None
    is_visited: bool
    project_id: uuid.UUID

class ResponseProjectDetail(ResponseProject):
    places: list[ResponsePlace] = []