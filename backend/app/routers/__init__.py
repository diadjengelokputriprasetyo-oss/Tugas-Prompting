from app.routers.auth import router as auth_router
from app.routers.predictions import router as predictions_router
from app.routers.users import router as users_router

__all__ = ["auth_router", "predictions_router", "users_router"]
