# Flask and extensions
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_login import current_user

# Local imports
from app.utils.auth_utils import (
    multi_auth_required,
    multi_auth_admin_required,
    _is_valid_api_key,
)
from app.utils.errors import (
    handle_errors,
    ValidationError,
    NotFoundError,
    ForbiddenError,
    ConflictError,
    UnauthorizedError,
)
from app.models.user import User
from app.models.base import db
from app.models.revoked_token import RevokedToken
from app.routes.auth import token_blocklist

user_bp = Blueprint("user", __name__)


@user_bp.route("/profile", methods=["GET"])
@multi_auth_required
@handle_errors
def get_profile():
    """Get current user profile (auth type and identity)."""
    # Check for JWT token
    try:
        verify_jwt_in_request(optional=True)
        jwt = get_jwt()
        if jwt:
            jti = jwt.get("jti")
            if (
                jti
                and not RevokedToken.is_token_revoked(jti)
                and jti not in token_blocklist
            ):
                return jsonify(
                    {
                        "auth_type": "jwt",
                        "id": jwt.get("sub"),
                        "username": jwt.get("username"),
                        "roles": jwt.get("roles"),
                    }
                )
    except Exception:
        pass  # JWT not present or invalid, continue to next auth method

    # Check for session auth
    if current_user.is_authenticated:
        return jsonify(
            {
                "auth_type": "session",
                "id": current_user.id,
                "username": current_user.username,
                "roles": current_user.roles,
            }
        )

    # Check for API key (constant-time comparison)
    api_key = request.headers.get("X-API-Key")
    if api_key and _is_valid_api_key(api_key):
        return jsonify({"auth_type": "api_key", "roles": "admin"})

    raise UnauthorizedError("Not authenticated")


@user_bp.route("/profile", methods=["PUT"])
@multi_auth_required
@handle_errors
def update_profile():
    """Update current user profile."""
    # Try JWT first
    try:
        verify_jwt_in_request(optional=True)
        jwt_identity = get_jwt_identity()
        if jwt_identity:
            user = db.session.get(User, int(jwt_identity))
            if user:
                return update_user_profile(user)
    except Exception:
        pass

    # Then try session auth
    if current_user and current_user.is_authenticated:
        return update_user_profile(current_user)

    raise NotFoundError("User not found")


def update_user_profile(user):
    """Apply profile updates and return response. Raises APIError on validation failure."""
    data = request.get_json() or {}
    if "username" in data:
        existing_user = User.query.filter_by(username=data["username"]).first()
        if existing_user and existing_user.id != user.id:
            raise ConflictError("Username already taken")
        user.username = data["username"]

    if "password" in data:
        if len(data["password"]) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        user.set_password(data["password"])

    db.session.commit()
    return make_response(
        jsonify(
            {
                "message": "Profile updated successfully",
                "user": {"id": user.id, "username": user.username, "roles": user.roles},
            }
        ),
        200,
    )


@user_bp.route("/users", methods=["GET"])
@multi_auth_admin_required
@handle_errors
def list_users():
    """List all users (admin only)."""
    users = User.query.all()
    return make_response(
        jsonify(
            [
                {"id": user.id, "username": user.username, "roles": user.roles}
                for user in users
            ]
        ),
        200,
    )


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@multi_auth_admin_required
@handle_errors
def update_user(user_id):
    """Update a user by ID (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    data = request.get_json() or {}
    if "password" in data:
        if len(data["password"]) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        user.set_password(data["password"])

    if "roles" in data:
        if data["roles"] not in ("user", "admin"):
            raise ValidationError("Invalid role")
        user.roles = data["roles"]

    db.session.commit()
    return make_response(
        jsonify(
            {
                "message": "User updated successfully",
                "user": {"id": user.id, "username": user.username, "roles": user.roles},
            }
        ),
        200,
    )


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@multi_auth_admin_required
@handle_errors
def delete_user(user_id):
    """Delete a user by ID (admin only)."""
    user = db.session.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    if user.roles == "admin" and User.query.filter_by(roles="admin").count() <= 1:
        raise ForbiddenError("Cannot delete the last admin user")

    db.session.delete(user)
    db.session.commit()
    return make_response(jsonify({"message": "User deleted successfully"}), 200)
