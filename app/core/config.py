from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl


# Application metadata
PROJECT_NAME = "FastAPI Example"


class Settings(BaseSettings):
    # API configuration
    API_V1_STR: str = "/api/v1"
    
    # CORS configuration
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000"  # Default Next.js port
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 