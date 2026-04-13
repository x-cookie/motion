"""HTTP and WebSocket client for Motion server.

This package provides type-safe HTTP and WebSocket clients for communicating with
the Motion API server. It handles authentication, error mapping,
and response conversion to domain DTOs.
"""

from motion_client.analytics_client import AnalyticsClient
from motion_client.audit_client import AuditClient
from motion_client.base_client import BaseApiClient
from motion_client.bulk_client import BulkClient
from motion_client.lifecycle_client import LifecycleClient
from motion_client.motion_api_client import MotionApiClient
from motion_client.notes_client import NotesClient
from motion_client.query_client import QueryClient
from motion_client.relationship_client import RelationshipClient
from motion_client.task_client import TaskClient
from motion_client.websocket import ConnectionState, WebSocketClient

__all__ = [
    "AnalyticsClient",
    "AuditClient",
    "BaseApiClient",
    "BulkClient",
    "ConnectionState",
    "LifecycleClient",
    "MotionApiClient",
    "NotesClient",
    "QueryClient",
    "RelationshipClient",
    "TaskClient",
    "WebSocketClient",
]
