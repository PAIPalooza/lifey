import uvicorn
from pathlib import Path

if __name__ == "__main__":
    # Add the project root to the Python path
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    
    # Run the FastAPI application
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )
