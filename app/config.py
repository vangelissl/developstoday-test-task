from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
	# Database 
	database_url: str = "sqlite+aiosqlite:///./travel.db"

	# External API
	aic_base_url: str = "https://api.artic.edu/api/v1"

	# App
	debug: bool = True

	auth_username: str = "admin"
	auth_password: str = "admin"

	model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")


settings = Settings()