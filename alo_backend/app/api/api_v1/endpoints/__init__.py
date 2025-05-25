# Import all endpoint routers to make them available when importing from app.api.api_v1.endpoints
from .auth import router as auth_router
from .users import router as users_router
from .events import router as events_router
from .reminders import router as reminders_router

__all__ = [
    "auth_router",
    "users_router",
    "events_router",
    "reminders_router",
]
