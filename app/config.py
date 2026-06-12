from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
	# Database 
	database_url: str = "sqlite+aiosqlite:///./travel.db"

	# External API
	aic_base_url: str = "https://api.artic.edu/api/v1"

	# App
	debug: bool = True
	cors_origins: list[str] = ["http://localhost:3000"]

	model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")


settings = Settings()