"""API routers for FastAPI endpoints."""

from motion_server.api.routers.analytics import router as analytics_router
from motion_server.api.routers.audit import router as audit_router
from motion_server.api.routers.bulk import router as bulk_router
from motion_server.api.routers.lifecycle import router as lifecycle_router
from motion_server.api.routers.notes import router as notes_router
from motion_server.api.routers.relationships import router as relationships_router
from motion_server.api.routers.tags import router as tags_router
from motion_server.api.routers.tasks import router as tasks_router
from motion_server.api.routers.websocket import router as websocket_router

__all__ = [
    "analytics_router",
    "audit_router",
    "bulk_router",
    "lifecycle_router",
    "notes_router",
    "relationships_router",
    "tags_router",
    "tasks_router",
    "websocket_router",
]
