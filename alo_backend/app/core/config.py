from typing import List, Optional, Union, Dict, Any
from functools import lru_cache
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import decouple, but handle if it's not available
try:
    from decouple import config
except ImportError:
    logger.warning("python-decouple not available, falling back to os.environ")
    # Define a simple fallback config function
    def config(key, default=None, cast=None):
        value = os.environ.get(key, default)
        if value is None:
            logger.warning(f"Environment variable {key} not found, using default")
            return default
        if cast and value is not None:
            try:
                return cast(value)
            except Exception as e:
                logger.error(f"Error casting {key}: {e}")
                return default
        return value

from pydantic import AnyHttpUrl, BaseModel, PostgresDsn, Field

class Settings(BaseModel):
    PROJECT_NAME: str = "ALO API"
    API_V1_STR: str = "/api/v1"
    
    # Database - Use multiple fallback approaches for maximum reliability
    DATABASE_URL: str = Field(
        default_factory=lambda: (
            os.environ.get("DATABASE_URL") or 
            config('DATABASE_URL', default=None) or
            'postgresql://postgres:postgres@localhost:5432/alo'
        )
    )
    
    # Log the database URL (masked for security)
    def __init__(self, **data: Any):
        super().__init__(**data)
        db_url = str(self.DATABASE_URL)
        masked_url = db_url.split('@')[0].split(':')[0] + ':****@' + db_url.split('@')[1] if '@' in db_url else 'default-local-db'
        logger.info(f"Using database: {masked_url}")
    
    # Security
    SECRET_KEY: str = Field(
        default_factory=lambda: (
            os.environ.get("SECRET_KEY") or 
            config('SECRET_KEY', default=None) or
            'dev-temp-secret-key-replace-in-production'
        )
    )
    ALGORITHM: str = Field(
        default_factory=lambda: (
            os.environ.get("ALGORITHM") or 
            config('ALGORITHM', default=None) or
            'HS256'
        )
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default_factory=lambda: (
            int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES") or 0) or 
            config('ACCESS_TOKEN_EXPIRE_MINUTES', default=60 * 24 * 7, cast=int) or
            60 * 24 * 7  # 7 days
        )
    )
    
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
