#!/usr/bin/env python
"""
WSGI entry point for ALO Backend
This file serves as the main entry point for various deployment platforms.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# Load environment variables from .env file if it exists
from dotenv import load_dotenv
dotenv_path = Path(__file__).resolve().parent / '.env'
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# Import the FastAPI app
from app.main import app

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
