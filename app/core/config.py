# we are using pydantic-settings in order to maintain the environment variables
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where your settings.py file is located
BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    DB_ECHO: bool
    API_V1_STR: str = "/api/v1"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

settings = Settings()