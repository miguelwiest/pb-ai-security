from .health import router as health_router
from .auth import router as auth_router
from .predict import router as predict_router

__all__ = ["health_router", "auth_router", "predict_router"]
