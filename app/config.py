from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# Database 
	database_url: str = "sqlite+aiosqlite:///./travel.db"

	# External API
	aic_base_url: str = "https://api.artic.edu/api/v1"

	# App
	debug: bool = False
	cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()