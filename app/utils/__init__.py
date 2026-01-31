# app/utils/__init__.py
"""Utility modules for the Toloka2Web application."""

from .auth_utils import multi_auth_required, multi_auth_admin_required
from .errors import (
    APIError,
    ValidationError,
    NotFoundError,
    UnauthorizedError,
    ForbiddenError,
    ConflictError,
    InternalError,
    ServiceUnavailableError,
    handle_errors,
    register_error_handlers,
)
from .responses import (
    success_response,
    created_response,
    no_content_response,
    paginated_response,
    error_response,
)
from .logging_config import configure_logging, get_logger

__all__ = [
    # Auth
    "multi_auth_required",
    "multi_auth_admin_required",
    # Errors
    "APIError",
    "ValidationError",
    "NotFoundError",
    "UnauthorizedError",
    "ForbiddenError",
    "ConflictError",
    "InternalError",
    "ServiceUnavailableError",
    "handle_errors",
    "register_error_handlers",
    # Responses
    "success_response",
    "created_response",
    "no_content_response",
    "paginated_response",
    "error_response",
    # Logging
    "configure_logging",
    "get_logger",
]
