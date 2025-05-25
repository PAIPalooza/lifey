import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.api.api_v1.api import api_router

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize resources
    print("Starting ALO API...")
    yield
    # Shutdown: Clean up resources
    print("Shutting down ALO API...")

def create_application() -> FastAPI:
    # Determine if we're in a production environment
    is_production = os.getenv("RAILWAY_ENVIRONMENT") == "production"
    
    # Check if we're using a placeholder database URL (Railway.com specific issue)
    db_url = settings.DATABASE_URL
    using_fallback_db = 'hostname' in db_url or 'port' in db_url
    
    # Configure OpenAPI with proper server URLs for different environments
    if is_production:
        # In production, dynamically set the server URL
        service_url = os.getenv("RAILWAY_PUBLIC_DOMAIN", "lifey-production.up.railway.app")
        servers = [
            {"url": f"https://{service_url}", "description": "Production server"}
        ]
    else:
        # In development, support multiple ports
        servers = [
            {"url": "http://localhost:8000", "description": "Development server - port 8000"},
            {"url": "http://localhost:8080", "description": "Development server - port 8080"}
        ]
    
    # Set documentation description based on database status
    if using_fallback_db:
        description = """
        # ⚠️ WARNING: DOCUMENTATION MODE ONLY ⚠️
        
        The application is running with a fallback in-memory database because a proper DATABASE_URL 
        has not been configured in the environment variables.
        
        **API calls requiring database access will not work until a valid DATABASE_URL is provided.**
        
        ## Configuration Instructions
        
        1. Set the DATABASE_URL environment variable in your Railway.com project settings
        2. Use a valid PostgreSQL connection string format: `postgresql://username:password@hostname:port/database`
        3. Restart the application after setting the environment variable
        
        ## Automated Life Organizer API
        
        Documentation is available at /docs regardless of the port.
        """
    else:
        description = "Automated Life Organizer API - Documentation is available at /docs regardless of the port."
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=description,
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
        openapi_url="/openapi.json",
        servers=servers
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

# Create FastAPI application
app = create_application()

@app.get("/")
async def root():
    return {"message": "Welcome to ALO API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
