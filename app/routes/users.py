from flask import Blueprint, jsonify, request, make_response, render_template
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_login import current_user
from app.utils.auth_utils import multi_auth_required, multi_auth_admin_required
from app.models.user import User
from app.models.base import db
from flask import current_app
from app.routes.auth import token_blocklist

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/profile', methods=['GET'])
@multi_auth_required
def get_profile():
    try:
        # Check for JWT token
        try:
            verify_jwt_in_request(optional=True)
            jwt = get_jwt()
            if jwt and jwt.get("jti") not in token_blocklist:
                return {
                    'auth_type': 'jwt',
                    'id': jwt.get("sub"),
                    'username': jwt.get("username"),
                    'roles': jwt.get("roles")
                }
        except Exception:
            pass  # JWT not present or invalid, continue to next auth method

        # Check for session auth
        if current_user.is_authenticated:
            return {
                'auth_type': 'session',
                'id': current_user.id,
                'username': current_user.username,
                'roles': current_user.roles
            }

        # Check for API key
        api_key = request.headers.get('X-API-Key')
        if api_key and api_key == current_app.config.get('API_KEY'):
            return {
                'auth_type': 'api_key',
                'roles': 'admin'  # API key has admin privileges
            }

        return {'error': 'Not authenticated'}, 401
    except Exception as e:
        return {'error': 'An error occurred while getting profile', 'details': str(e)}, 500

@user_bp.route('/api/profile', methods=['PUT'])
@multi_auth_required
def update_profile():
    try:
        # Try JWT first
        try:
            verify_jwt_in_request(optional=True)
            jwt_identity = get_jwt_identity()
            if jwt_identity:
                user = User.query.get(int(jwt_identity))
                if user:
                    return update_user_profile(user)
        except Exception:
            pass

        # Then try session auth
        if current_user and current_user.is_authenticated:
            return update_user_profile(current_user)

        return make_response(jsonify({"error": "User not found"}), 404)
    except Exception as e:
        db.session.rollback()
        error_message = {
            "error": "Failed to update profile",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

def update_user_profile(user):
    data = request.get_json()
    if 'username' in data:
        # Check if username is already taken
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user.id:
            return make_response(jsonify({"error": "Username already taken"}), 400)
        user.username = data['username']
        
    if 'password' in data:
        if len(data['password']) < 8:
            return make_response(jsonify({"error": "Password must be at least 8 characters long"}), 400)
        user.set_password(data['password'])
        
    db.session.commit()
    return make_response(jsonify({
        "message": "Profile updated successfully",
        "user": {
            "id": user.id,
            "username": user.username,
            "roles": user.roles
        }
    }), 200)

@user_bp.route('/api/users', methods=['GET'])
@multi_auth_admin_required
def list_users():
    try:
        users = User.query.all()
        return make_response(jsonify([{
            "id": user.id,
            "username": user.username,
            "roles": user.roles
        } for user in users]), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to list users",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@multi_auth_admin_required
def update_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
            
        data = request.get_json()
        if 'password' in data:
            if len(data['password']) < 8:
                return make_response(jsonify({"error": "Password must be at least 8 characters long"}), 400)
            user.set_password(data['password'])
            
        if 'roles' in data:
            # Validate roles
            if data['roles'] not in ['user', 'admin']:
                return make_response(jsonify({"error": "Invalid role"}), 400)
            user.roles = data['roles']
            
        db.session.commit()
        return make_response(jsonify({
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "roles": user.roles
            }
        }), 200)
    except Exception as e:
        db.session.rollback()
        error_message = {
            "error": "Failed to update user",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@multi_auth_admin_required
def delete_user(user_id):
    try:
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)
            
        # Prevent deleting the last admin
        if user.roles == 'admin' and User.query.filter_by(roles='admin').count() <= 1:
            return make_response(jsonify({"error": "Cannot delete the last admin user"}), 400)
            
        db.session.delete(user)
        db.session.commit()
        return make_response(jsonify({"message": "User deleted successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        error_message = {
            "error": "Failed to delete user",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500) 