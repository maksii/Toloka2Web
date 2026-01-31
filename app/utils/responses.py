"""Standardized response utilities for the API.

This module provides helper functions for creating consistent
API responses throughout the application.
"""

from typing import Any, Optional

from flask import jsonify


def success_response(
    data: Any = None, message: Optional[str] = None, status: int = 200
):
    """Create a standardized success response.

    Args:
        data: Response payload (can be any JSON-serializable type)
        message: Optional success message
        status: HTTP status code (default 200)

    Returns:
        Tuple of (response, status_code)

    Example:
        return success_response({'user': user_data}, message='User created')
    """
    response = {}

    if data is not None:
        response["data"] = data

    if message:
        response["message"] = message

    return jsonify(response), status


def created_response(data: Any = None, message: str = "Resource created"):
    """Create a 201 Created response.

    Args:
        data: Created resource data
        message: Success message

    Returns:
        Tuple of (response, 201)
    """
    return success_response(data=data, message=message, status=201)


def no_content_response():
    """Create a 204 No Content response.

    Returns:
        Tuple of ('', 204)
    """
    return "", 204


def paginated_response(
    items: list,
    total: int,
    page: int = 1,
    per_page: int = 20,
    message: Optional[str] = None,
):
    """Create a paginated response.

    Args:
        items: List of items for current page
        total: Total number of items across all pages
        page: Current page number (1-indexed)
        per_page: Items per page
        message: Optional message

    Returns:
        Tuple of (response, 200)

    Example:
        items = get_items(page=2, per_page=10)
        total = get_total_count()
        return paginated_response(items, total, page=2, per_page=10)
    """
    pages = (total + per_page - 1) // per_page if per_page > 0 else 0

    response = {
        "data": items,
        "meta": {
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": pages,
            "has_next": page < pages,
            "has_prev": page > 1,
        },
    }

    if message:
        response["message"] = message

    return jsonify(response), 200


def error_response(code: str, message: str, status: int = 400, details: Any = None):
    """Create a standardized error response.

    This is a lower-level function. For most cases, prefer using
    the exception classes from app.utils.errors instead.

    Args:
        code: Machine-readable error code
        message: Human-readable error message
        status: HTTP status code
        details: Optional error details

    Returns:
        Tuple of (response, status_code)

    Example:
        return error_response('VALIDATION_ERROR', 'Invalid email format', 400)
    """
    error = {"code": code, "message": message}

    if details:
        error["details"] = details

    return jsonify(error=error), status
