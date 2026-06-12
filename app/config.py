from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	# App
	debug: bool = False
	cors_origins: list[str] = ["http://localhost:3000"]


settings = Settings()