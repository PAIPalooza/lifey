#!/usr/bin/env python
"""
Development server entry point for ALO Backend
This file is used for local development only.
For production deployment, use wsgi.py instead.
"""

import os
import sys
import logging
import uvicorn
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
    
    # Set default environment variables for local development
    default_env_vars = {
        "DATABASE_URL": "postgresql://postgres:postgres@localhost:5432/alo",
        "SECRET_KEY": "dev-temp-secret-key-for-local-development-only",
        "ALGORITHM": "HS256",
        "ACCESS_TOKEN_EXPIRE_MINUTES": "10080"  # 7 days
    }
    
    # Set environment variables if not already set
    for key, value in default_env_vars.items():
        if key not in os.environ:
            logger.info(f"Setting default environment variable: {key}")
            os.environ[key] = value
    
    # Try to load from .env file if it exists (overriding defaults)
    try:
        from dotenv import load_dotenv
        dotenv_path = Path(__file__).resolve().parent / '.env'
        if dotenv_path.exists():
            logger.info(f"Loading environment variables from {dotenv_path}")
            load_dotenv(dotenv_path, override=True)
        else:
            logger.info(".env file not found, using defaults and environment variables")
    except ImportError:
        logger.warning("python-dotenv not available, skipping .env file loading")
    
    # Import the app to validate it loads correctly
    logger.info("Importing FastAPI application")
    from app.main import app
    logger.info("FastAPI application successfully imported")
    
    if __name__ == "__main__":
        # Run the FastAPI application
        logger.info(f"Starting development server on port {os.environ.get('PORT', '8000')}")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", "8000")),
            reload=True,
            reload_dirs=["app"],
            log_level="info"
        )

except Exception as e:
    logger.critical(f"Failed to initialize application: {str(e)}", exc_info=True)
    # Re-raise the exception to ensure the application fails to start
    raise
