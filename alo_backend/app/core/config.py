from typing import List, Optional
from functools import lru_cache
import os
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from decouple import config
except ImportError:
    logger.warning("python-decouple not installed, falling back to os.environ")
    # Define a simple config function as fallback
    def config(key, default=None, cast=None):
        value = os.environ.get(key, default)
        if value is not None and cast is not None:
            try:
                value = cast(value)
            except Exception as e:
                logger.error(f"Error casting {key}: {e}")
                return default
        return value

from pydantic import AnyHttpUrl, BaseModel, validator


def validate_database_url(v: Optional[str]) -> str:
    """Validate and format database URL to ensure it's properly formatted"""
    if not v:
        # Fallback to a default that should work locally
        default_url = 'postgresql://postgres:postgres@localhost:5432/alo'
        logger.warning(f"No DATABASE_URL provided, using default: {default_url.replace('postgres:postgres', 'postgres:****')}")
        return default_url
    
    # Special handling for Railway.com placeholder format
    # Railway might provide URLs with placeholders like postgresql://user:pass@hostname:port/database
    if '@hostname:port/' in v or 'hostname' in v or 'port' in v:
        logger.info("Detected Railway.com placeholder URL format, using default port")
        # Extract user and password if possible
        try:
            # Handle the case where hostname:port are placeholders
            if '@hostname:port/' in v:
                parts = v.split('@')
                user_pass = parts[0].split('://')
                if len(user_pass) > 1:
                    auth = user_pass[1]
                    db_name = parts[1].split('/')[1]
                    # Construct URL with proper port
                    return f"postgresql://{auth}@localhost:5432/{db_name}"
            
            # If the URL contains 'hostname' but not in the expected format,
            # or if it contains 'port' as a literal string instead of a number
            logger.warning("Could not parse Railway.com URL format, using local default")
            return 'postgresql://postgres:postgres@localhost:5432/alo'
        except Exception as e:
            logger.error(f"Error parsing Railway.com URL format: {str(e)}")
            return 'postgresql://postgres:postgres@localhost:5432/alo'
    
    # Check if it appears to be another Railway.com URL format
    if 'railway' in v.lower():
        logger.info("Using Railway.com database URL")
        return v
    
    # Try to validate a standard PostgreSQL URL
    try:
        # Simple regex validation for postgres URL format
        pattern = r'^postgresql://([^:]+):([^@]+)@([^:]+):([^/]+)/(.+)$'
        if not re.match(pattern, v):
            logger.warning(f"DATABASE_URL doesn't match expected format, returning as-is")
            return v
            
        # Extract components to validate the port
        match = re.match(pattern, v)
        if match:
            user, password, host, port, dbname = match.groups()
            try:
                # Try to parse port as integer
                port_int = int(port)
                # Reconstruct URL to ensure it's properly formatted
                masked_url = f"postgresql://{user}:****@{host}:{port_int}/{dbname}"
                logger.info(f"Validated database URL: {masked_url}")
                return f"postgresql://{user}:{password}@{host}:{port_int}/{dbname}"
            except ValueError:
                logger.warning(f"Non-numeric port in DATABASE_URL: {port}, using default port 5432")
                # Use default port if the port is invalid
                return f"postgresql://{user}:{password}@{host}:5432/{dbname}"
    except Exception as e:
        logger.error(f"Error validating DATABASE_URL: {str(e)}")
        
    # Return a working default if we can't validate/fix it
    logger.warning("Could not validate DATABASE_URL format, using default")
    return 'postgresql://postgres:postgres@localhost:5432/alo'

class Settings(BaseModel):
    PROJECT_NAME: str = "ALO API"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str = config('DATABASE_URL', default='postgresql://postgres:postgres@localhost:5432/alo')
    
    @validator("DATABASE_URL")
    def validate_db_url(cls, v):
        return validate_database_url(v)

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
