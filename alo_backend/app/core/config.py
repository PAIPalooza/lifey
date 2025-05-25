from typing import List
from functools import lru_cache
import os

from decouple import config
from pydantic import AnyHttpUrl, BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "ALO API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = config('DATABASE_URL', default='postgresql://postgres:postgres@localhost:5432/alo')
    
    # Security
    SECRET_KEY: str = config('SECRET_KEY', default='your-secret-key-here')
    ALGORITHM: str = config('ALGORITHM', default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=60 * 24 * 7, cast=int)  # 7 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Default React port
        "http://localhost:8000",  # Default FastAPI port
    ]
    
    # First superuser
    FIRST_SUPERUSER_EMAIL: str = config('FIRST_SUPERUSER_EMAIL', default='admin@example.com')
    FIRST_SUPERUSER_PASSWORD: str = config('FIRST_SUPERUSER_PASSWORD', default='adminpassword')

@lru_cache()
def get_settings() -> Settings:
    return Settings()
