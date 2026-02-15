"""Configuration management using pydantic-settings"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # Server settings
    APP_NAME: str = "Remotion FastAPI Server"
    VERSION: str = "1.0.0"
    DEBUG: bool = False

    # API settings
    API_PREFIX: str = "/api/v1"
    MAX_CONCURRENT_RENDERS: int = 2

    # Storage settings
    OUTPUT_DIR: str = "./outputs"
    BASE_URL: str = "http://localhost:8000"

    # Browser pool settings
    MAX_BROWSER_INSTANCES: int = 3
    MAX_BROWSER_IDLE_SECONDS: int = 300

    # Queue settings
    JOB_CLEANUP_HOURS: int = 24

    # Node.js settings
    NODE_PATH: str = "node"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
