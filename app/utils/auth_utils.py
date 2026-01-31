"""Authentication utilities for multi-method auth support."""
import secrets
from functools import wraps

from flask import jsonify, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_login import current_user

from app.models.revoked_token import RevokedToken


def _is_valid_api_key(provided_key: str) -> bool:
    """Check if the provided API key is valid using constant-time comparison.
    
    Uses secrets.compare_digest to prevent timing attacks.
    
    Args:
        provided_key: The API key provided in the request
        
    Returns:
        True if the key is valid, False otherwise
    """
    expected_key = current_app.config.get('API_KEY', '')
    if not provided_key or not expected_key:
        return False
    
    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(provided_key, expected_key)


def multi_auth_required(fn):
    """Decorator that allows multiple authentication methods.
    
    Checks in order:
    1. JWT token (if valid and not revoked)
    2. Session authentication (Flask-Login)
    3. API key (X-API-Key header)
    
    Returns 401 if none of the methods succeed.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First, check for JWT token
        try:
            verify_jwt_in_request(optional=True)
            jwt = get_jwt()
            if jwt:
                jti = jwt.get("jti")
                if jti and not RevokedToken.is_token_revoked(jti):
                    return fn(*args, **kwargs)
        except Exception:
            pass  # JWT not present or invalid, continue to next auth method

        # Then check for session auth
        if current_user and current_user.is_authenticated:
            return fn(*args, **kwargs)

        # Finally check for API key (using constant-time comparison)
        api_key = request.headers.get('X-API-Key')
        if api_key and _is_valid_api_key(api_key):
            return fn(*args, **kwargs)

        return jsonify({"error": "Authentication required"}), 401

    return wrapper


def multi_auth_admin_required(fn):
    """Decorator that requires admin privileges via multiple auth methods.
    
    Checks in order:
    1. JWT token with admin role
    2. Session authentication with admin role
    3. API key (always has admin privileges)
    
    Returns 401 if not authenticated, 403 if authenticated but not admin.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First, check for JWT token
        try:
            verify_jwt_in_request(optional=True)
            jwt = get_jwt()
            if jwt:
                jti = jwt.get("jti")
                if jti and not RevokedToken.is_token_revoked(jti):
                    if jwt.get("roles") == "admin":
                        return fn(*args, **kwargs)
                    return jsonify({"error": "Admin privileges required"}), 403
        except Exception:
            pass  # JWT not present or invalid, continue to next auth method

        # Then check for session auth
        if current_user and current_user.is_authenticated:
            if current_user.roles == "admin":
                return fn(*args, **kwargs)
            return jsonify({"error": "Admin privileges required"}), 403

        # Finally check for API key (using constant-time comparison)
        # API key always has admin privileges
        api_key = request.headers.get('X-API-Key')
        if api_key and _is_valid_api_key(api_key):
            return fn(*args, **kwargs)

        return jsonify({"error": "Authentication required"}), 401

    return wrapper
