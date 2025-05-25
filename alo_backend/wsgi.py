#!/usr/bin/env python
"""
WSGI entry point for ALO Backend
This file serves as the main entry point for various deployment platforms.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

try:
    # Add the project root to the Python path
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    logger.info(f"Added {Path(__file__).resolve().parent} to Python path")
    
    # Set default environment variables if not present
    default_env_vars = {
        "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/alo",
        "SECRET_KEY": "dev-temp-secret-key-replace-in-production",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "10080"  # 7 days
    }
    
    # Set environment variables if not already set
    for key, value in default_env_vars.items():
        if key not in os.environ:
            logger.info(f"Setting default environment variable: {key}")
            os.environ[key] = value
    
    # Try to load from .env file if it exists
    try:
        from dotenv import load_dotenv
        dotenv_path = Path(__file__).resolve().parent / '.env'
        if dotenv_path.exists():
            logger.info(f"Loading environment variables from {dotenv_path}")
            load_dotenv(dotenv_path)
        else:
            logger.info(".env file not found, using defaults and environment variables")
    except ImportError:
        logger.warning("python-dotenv not available, skipping .env file loading")
    
    # Log all environment variables (with sensitive data masked)
    for key in ["DATABASE_URL", "SECRET_KEY"]:
        if key in os.environ:
            masked_value = "****" if key == "SECRET_KEY" else os.environ[key].split("@")[0].split(":")[0] + ":****@" + os.environ[key].split("@")[1] if "@" in os.environ[key] else "****"
            logger.info(f"Environment variable {key}: {masked_value}")
    
    # Import the FastAPI app
    logger.info("Importing FastAPI application")
    from app.main import app
    logger.info("FastAPI application successfully imported")
    
except Exception as e:
    logger.critical(f"Failed to initialize application: {str(e)}", exc_info=True)
    # Re-raise the exception to ensure the application fails to start
    raise

# This allows the file to be used by Gunicorn or other WSGI servers
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
        log_level="info"
    )
