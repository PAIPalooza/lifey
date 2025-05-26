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
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Enable documentation optimization mode if accessing docs
# This significantly improves Swagger documentation load time
def is_docs_request(path_info):
    """Check if this is a documentation-related request"""
    docs_paths = [
        '/docs', '/redoc', '/openapi.json'
    ]
    return any(path_info.startswith(path) for path in docs_paths)

# Set environment variable for deferred database initialization
# This optimizes for faster documentation access
if 'PATH_INFO' in os.environ and is_docs_request(os.environ['PATH_INFO']):
    logger.info(f"Documentation request detected: {os.environ['PATH_INFO']}")
    os.environ['DEFER_DB_INIT'] = 'true'
    logger.info("Enabling deferred database initialization for faster docs loading")

# Import the FastAPI app
from app.main import app

# This allows the file to be used by Gunicorn or other WSGI servers
if __name__ == "__main__":
    import uvicorn
    # Railway.com uses port 8080 by default
    port = int(os.getenv("PORT", "8080"))
    
    logger.info(f"Starting ALO API on port {port}")
    logger.info(f"API documentation available at: http://localhost:{port}/docs")
    logger.info(f"ReDoc documentation available at: http://localhost:{port}/redoc")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info"
    )
