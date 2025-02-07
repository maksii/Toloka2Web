from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask_login import current_user
from app.routes.auth import token_blocklist

def multi_auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First, check for JWT token
        try:
            verify_jwt_in_request(optional=True)
            jwt = get_jwt()
            if jwt and jwt.get("jti") not in token_blocklist:
                return fn(*args, **kwargs)
        except Exception:
            pass  # JWT not present or invalid, continue to next auth method

        # Then check for session auth
        if current_user and current_user.is_authenticated:
            return fn(*args, **kwargs)

        # Finally check for API key
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == current_app.config.get('API_KEY'):
            return fn(*args, **kwargs)

        return jsonify({"error": "Authentication required"}), 401

    return wrapper

def multi_auth_admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # First, check for JWT token
        try:
            verify_jwt_in_request(optional=True)
            jwt = get_jwt()
            if jwt and jwt.get("jti") not in token_blocklist:
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

        # Finally check for API key
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == current_app.config.get('API_KEY'):
            return fn(*args, **kwargs)

        return jsonify({"error": "Authentication required"}), 401

    return wrapper 