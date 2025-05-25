from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, users, events, reminders

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(reminders.router, prefix="/reminders", tags=["Reminders"])
