from typing import List

from .base import Base

from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, UUID, DateTime, String, Boolean, ForeignKey

import uuid

class ProjectModel(Base):
	__tablename__ = "projects"
	id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
	name: Mapped[str] = mapped_column(String, nullable=False)
	description: Mapped[str | None] = mapped_column(String, nullable=True)
	start_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
	is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
	places: Mapped[List["PlaceModel"]] = relationship(back_populates="project")


class PlaceModel(Base):
	__tablename__ = "places"
	id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, default=uuid.uuid4)
	external_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
	title: Mapped[str] = mapped_column(String, nullable=False)
	artist: Mapped[str | None] = mapped_column(String, nullable=True)
	image_url: Mapped[str | None] = mapped_column(String, nullable=True)
	notes: Mapped[str | None] = mapped_column(String, nullable=True)
	is_visited: Mapped[bool] = mapped_column(Boolean, default=False)
	project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
	project: Mapped["ProjectModel"] = relationship(back_populates="places")
	 