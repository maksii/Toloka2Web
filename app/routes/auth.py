# Standard library imports
import secrets

# Flask and extensions
from flask import Blueprint, jsonify, request, current_app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
)
from flask_login import current_user
from sqlalchemy.exc import IntegrityError

# Local imports
from app.models.user import User
from app.models.application_settings import ApplicationSettings
from app.models.revoked_token import RevokedToken
from app.models.base import db
from app.utils.errors import (
    handle_errors,
    ValidationError,
    UnauthorizedError,
    NotFoundError,
    ForbiddenError,
    ConflictError,
    InternalError,
)

auth_bp = Blueprint("auth", __name__)

# Legacy token blocklist for backward compatibility
# New code should use RevokedToken model directly
token_blocklist = set()


def _is_valid_api_key(provided_key: str) -> bool:
    """Check if the provided API key is valid using constant-time comparison.

    Args:
        provided_key: The API key provided in the request

    Returns:
        True if the key is valid, False otherwise
    """
    expected_key = current_app.config.get("API_KEY", "")
    if not provided_key or not expected_key:
        return False
    return secrets.compare_digest(provided_key, expected_key)


def check_auth():
    """Check authentication status using multiple methods.

    Checks in order: JWT token, session auth, API key.

    Returns:
        dict: Authentication info or error response
    """
    try:
        # Check for JWT token
        try:
            verify_jwt_in_request(optional=True)
            jwt = get_jwt()
            if jwt:
                jti = jwt.get("jti")
                # Check both in-memory and database blocklist
                if (
                    jti
                    and not RevokedToken.is_token_revoked(jti)
                    and jti not in token_blocklist
                ):
                    return {
                        "auth_type": "jwt",
                        "id": jwt.get("sub"),
                        "username": jwt.get("username"),
                        "roles": jwt.get("roles"),
                    }
        except Exception:
            pass  # JWT not present or invalid, continue to next auth method

        # Check for session auth
        if current_user.is_authenticated:
            return {
                "auth_type": "session",
                "id": current_user.id,
                "username": current_user.username,
                "roles": current_user.roles,
            }

        # Check for API key (using constant-time comparison)
        api_key = request.headers.get("X-API-Key")
        if api_key and _is_valid_api_key(api_key):
            return {
                "auth_type": "api_key",
                "roles": "admin",  # API key has admin privileges
            }

        raise UnauthorizedError("Not authenticated")
    except UnauthorizedError:
        raise
    except Exception as e:
        raise InternalError(
            "An error occurred while checking authentication", details=str(e)
        )


@auth_bp.route("/auth/register", methods=["POST"])
@handle_errors
def register():
    """Register a new user."""
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        raise ValidationError("Username and password are required")

    # Check if registration is open
    open_registration = ApplicationSettings.query.filter_by(
        key="open_registration"
    ).first()
    if (
        not getattr(open_registration, "value", None)
        or open_registration.value.lower() != "true"
    ):
        raise ForbiddenError("Registration is currently closed")

    # Validate password strength
    password = data["password"]
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long")

    # Create new user
    user = User(username=data["username"])
    user.set_password(password)

    # First user gets admin role
    user.roles = "admin" if User.query.count() == 0 else "user"

    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ConflictError("Username already exists")

    return jsonify(
        {
            "message": "User registered successfully",
            "user": {"id": user.id, "username": user.username, "roles": user.roles},
        }
    ), 201


@auth_bp.route("/auth/login", methods=["POST"])
@handle_errors
def login():
    """Authenticate user and return JWT tokens."""
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        raise ValidationError("Username and password are required")

    user = User.query.filter_by(username=data["username"]).first()

    if user and user.check_password(data["password"]):
        access_token = create_access_token(
            identity=str(user.id),  # Convert ID to string
            additional_claims={"username": user.username, "roles": user.roles},
        )
        refresh_token = create_refresh_token(
            identity=str(user.id),  # Convert ID to string
            additional_claims={"username": user.username, "roles": user.roles},
        )

        response = jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {"id": user.id, "username": user.username, "roles": user.roles},
            }
        )

        # Set cookies for enhanced security (optional, frontend can also store in memory)
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)

        return response

    raise UnauthorizedError("Invalid username or password")


@auth_bp.route("/auth/refresh", methods=["POST"])
@jwt_required(refresh=True)
@handle_errors
def refresh():
    """Refresh an access token using a refresh token."""
    current_user_id = get_jwt_identity()
    jwt = get_jwt()

    # Check if token is in blocklist (both in-memory and database)
    token_id = jwt.get("jti")
    if token_id in token_blocklist or RevokedToken.is_token_revoked(token_id):
        raise UnauthorizedError("Token has been revoked")

    user = User.query.get(int(current_user_id))  # Convert string ID back to int

    if not user:
        raise NotFoundError("User not found")

    access_token = create_access_token(
        identity=str(user.id),  # Convert ID to string
        additional_claims={"username": user.username, "roles": user.roles},
    )

    response = jsonify(
        {
            "access_token": access_token,
            "user": {"id": user.id, "username": user.username, "roles": user.roles},
        }
    )

    set_access_cookies(response, access_token)
    return response


@auth_bp.route("/auth/logout", methods=["POST"])
@jwt_required(verify_type=False)
@handle_errors
def logout():
    """Log out by revoking the current JWT token."""
    jwt = get_jwt()
    token_id = jwt.get("jti")

    # Store in database for persistence
    RevokedToken.revoke_token(token_id)
    # Also add to in-memory set for immediate effect
    token_blocklist.add(token_id)

    response = jsonify({"message": "Successfully logged out"})
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/auth/me", methods=["GET"])
@jwt_required()
@handle_errors
def me():
    """Get current user information."""
    current_user_id = get_jwt_identity()
    jwt = get_jwt()

    # Check if token is in blocklist (both in-memory and database)
    token_id = jwt.get("jti")
    if token_id in token_blocklist or RevokedToken.is_token_revoked(token_id):
        raise UnauthorizedError("Token has been revoked")

    user = User.query.get(int(current_user_id))  # Convert string ID back to int

    if not user:
        raise NotFoundError("User not found")

    return jsonify({"id": user.id, "username": user.username, "roles": user.roles})


@auth_bp.route("/auth/change-password", methods=["POST"])
@jwt_required()
@handle_errors
def change_password():
    """Change the current user's password."""
    current_user_id = get_jwt_identity()
    jwt = get_jwt()

    # Check if token is in blocklist (both in-memory and database)
    token_id = jwt.get("jti")
    if token_id in token_blocklist or RevokedToken.is_token_revoked(token_id):
        raise UnauthorizedError("Token has been revoked")

    data = request.get_json()
    if not data or not data.get("current_password") or not data.get("new_password"):
        raise ValidationError("Current password and new password are required")

    user = User.query.get(int(current_user_id))  # Convert string ID back to int
    if not user:
        raise NotFoundError("User not found")

    if not user.check_password(data["current_password"]):
        raise UnauthorizedError("Current password is incorrect")

    # Validate new password
    if len(data["new_password"]) < 8:
        raise ValidationError("New password must be at least 8 characters long")

    user.set_password(data["new_password"])
    db.session.commit()

    # Invalidate current token (persist to database)
    RevokedToken.revoke_token(token_id)
    token_blocklist.add(token_id)

    return jsonify({"message": "Password changed successfully"}), 200


# JWT token callbacks
@auth_bp.route("/auth/validate", methods=["POST"])
@jwt_required(verify_type=False)
@handle_errors
def validate_token():
    """Validate if a JWT token is still valid and not revoked."""
    jwt = get_jwt()
    token_id = jwt.get("jti")

    # Check both in-memory and database blocklist
    if token_id in token_blocklist or RevokedToken.is_token_revoked(token_id):
        raise UnauthorizedError("Token has been revoked")

    return jsonify({"valid": True}), 200
