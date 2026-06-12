from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# Database 
	database_url: str = "sqlite+aiosqlite:///./travel.db"

	# App
	debug: bool = False
	cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()