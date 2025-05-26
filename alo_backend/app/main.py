import os
import logging
from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager

# Configure logging
logger = logging.getLogger(__name__)

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

# Custom documentation routes for faster loading
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html(request: Request):
    logger.info("Serving custom Swagger UI with faster loading")
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
    )

@app.get("/openapi.json", include_in_schema=False)
async def get_openapi_endpoint():
    logger.info("Serving OpenAPI schema with faster loading")
    return JSONResponse(get_openapi(title=app.title, version=app.version, routes=app.routes))

@app.get("/")
async def root():
    return {"message": "Welcome to ALO API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
