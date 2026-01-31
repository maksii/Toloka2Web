"""Standardized error handling for the API.

This module provides:
- Base APIError exception class
- Specific error subclasses for common HTTP error codes
- Error handler decorator for routes
- Flask error handlers for consistent error responses
"""

from functools import wraps
from typing import Any, Dict, Optional

from flask import jsonify, current_app


class APIError(Exception):
    """Base exception class for API errors.

    All API errors should inherit from this class to ensure consistent
    error response format across the application.

    Attributes:
        code: Machine-readable error code (e.g., 'VALIDATION_ERROR')
        message: Human-readable error message
        status: HTTP status code
        details: Optional additional error details (only in debug mode)
    """

    def __init__(
        self, code: str, message: str, status: int = 400, details: Optional[Any] = None
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.details = details

    def to_dict(self, include_details: bool = False) -> Dict:
        """Convert error to dictionary for JSON response.

        Args:
            include_details: Whether to include error details

        Returns:
            Dictionary representation of the error
        """
        error_dict = {"code": self.code, "message": self.message}
        if include_details and self.details:
            error_dict["details"] = self.details
        return error_dict

    def to_response(self):
        """Convert error to Flask JSON response.

        Returns:
            Tuple of (response, status_code)
        """
        include_details = current_app.debug if current_app else False
        return jsonify(error=self.to_dict(include_details)), self.status


class ValidationError(APIError):
    """Error for invalid input data."""

    def __init__(self, message: str, details: Optional[Any] = None):
        super().__init__(
            code="VALIDATION_ERROR", message=message, status=400, details=details
        )


class NotFoundError(APIError):
    """Error for resources that don't exist."""

    def __init__(
        self, message: str = "Resource not found", details: Optional[Any] = None
    ):
        super().__init__(code="NOT_FOUND", message=message, status=404, details=details)


class UnauthorizedError(APIError):
    """Error for unauthenticated requests."""

    def __init__(
        self, message: str = "Authentication required", details: Optional[Any] = None
    ):
        super().__init__(
            code="UNAUTHORIZED", message=message, status=401, details=details
        )


class ForbiddenError(APIError):
    """Error for unauthorized access to resources."""

    def __init__(self, message: str = "Access denied", details: Optional[Any] = None):
        super().__init__(code="FORBIDDEN", message=message, status=403, details=details)


class ConflictError(APIError):
    """Error for resource conflicts (e.g., duplicate entries)."""

    def __init__(
        self, message: str = "Resource conflict", details: Optional[Any] = None
    ):
        super().__init__(code="CONFLICT", message=message, status=409, details=details)


class InternalError(APIError):
    """Error for internal server errors."""

    def __init__(
        self, message: str = "Internal server error", details: Optional[Any] = None
    ):
        super().__init__(
            code="INTERNAL_ERROR", message=message, status=500, details=details
        )


class ServiceUnavailableError(APIError):
    """Error for external service failures (MAL, TMDB, etc.)."""

    def __init__(
        self,
        message: str = "Service temporarily unavailable",
        details: Optional[Any] = None,
    ):
        super().__init__(
            code="SERVICE_UNAVAILABLE", message=message, status=503, details=details
        )


def handle_errors(fn):
    """Decorator that catches exceptions and returns consistent error responses.

    This decorator catches APIError exceptions and converts them to JSON responses.
    Other exceptions are logged and converted to internal server errors.

    Usage:
        @handle_errors
        def my_route():
            if not valid:
                raise ValidationError('Invalid data')
            return jsonify(data)
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except APIError as e:
            # Log the error
            current_app.logger.warning(
                f"API Error: {e.code} - {e.message}",
                extra={"error_code": e.code, "status": e.status},
            )
            return e.to_response()
        except Exception as e:
            # Log unexpected errors
            current_app.logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            error = InternalError(
                message="An unexpected error occurred",
                details=str(e) if current_app.debug else None,
            )
            return error.to_response()

    return wrapper


def register_error_handlers(app):
    """Register Flask error handlers for consistent error responses.

    This should be called during app initialization to ensure all
    unhandled errors return consistent JSON responses.

    Args:
        app: Flask application instance
    """

    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle APIError exceptions."""
        app.logger.warning(
            f"API Error: {error.code} - {error.message}",
            extra={"error_code": error.code, "status": error.status},
        )
        return error.to_response()

    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request errors."""
        return jsonify(error={"code": "BAD_REQUEST", "message": "Bad request"}), 400

    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized errors."""
        return jsonify(
            error={"code": "UNAUTHORIZED", "message": "Authentication required"}
        ), 401

    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 Forbidden errors."""
        return jsonify(error={"code": "FORBIDDEN", "message": "Access denied"}), 403

    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found errors."""
        return jsonify(
            error={"code": "NOT_FOUND", "message": "Resource not found"}
        ), 404

    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server Error."""
        app.logger.error(f"Internal server error: {error}", exc_info=True)
        return jsonify(
            error={"code": "INTERNAL_ERROR", "message": "Internal server error"}
        ), 500
