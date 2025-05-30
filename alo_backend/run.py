#!/usr/bin/env python
"""
Development server entry point for ALO Backend
This file is used for local development only.
For production deployment, use wsgi.py instead.
"""

import os
import uvicorn
from pathlib import Path

# Add the project root to the Python path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Import the app to validate it loads correctly
from app.main import app

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )
