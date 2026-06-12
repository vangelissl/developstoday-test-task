from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from contextlib import asynccontextmanager

from .config import settings
from .database import engine
from app.domain.base import Base

from app.routers.project_router import router as project_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app(lifespan) -> FastAPI:
    application = FastAPI(
        title="Travel Planner",
        version="0.1.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url=None,
        lifespan=lifespan
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    application.include_router(project_router)

    if settings.debug:
        @application.get("/health")
        async def health_check() -> dict[str, str]:
            return {"status": "ok"}

    return application


app = create_app(lifespan=lifespan)
