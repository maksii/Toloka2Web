from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request, make_response, current_app
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    get_jwt_identity, jwt_required,
    get_jwt, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,
    verify_jwt_in_request
)
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

from app.models.user import User
from app.models.application_settings import ApplicationSettings
from app.models.base import db

auth_bp = Blueprint('auth', __name__)

# Token blocklist for logged out tokens
token_blocklist = set()

def check_auth():
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
        return {
            'error': 'An error occurred while checking authentication',
            'details': str(e)
        }, 500

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        # Check if registration is open
        open_registration = ApplicationSettings.query.filter_by(key='open_registration').first()
        if not getattr(open_registration, 'value', None) or open_registration.value.lower() != 'true':
            return jsonify({'error': 'Registration is currently closed'}), 403

        # Validate password strength
        password = data['password']
        if len(password) < 8:
            return jsonify({'error': 'Password must be at least 8 characters long'}), 400
        
        # Create new user
        user = User(username=data['username'])
        user.set_password(password)
        
        # First user gets admin role
        user.roles = 'admin' if User.query.count() == 0 else 'user'
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return jsonify({'error': 'Username already exists'}), 409
            
        return jsonify({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'roles': user.roles
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            access_token = create_access_token(
                identity=str(user.id),  # Convert ID to string
                additional_claims={
                    'username': user.username,
                    'roles': user.roles
                }
            )
            refresh_token = create_refresh_token(
                identity=str(user.id),  # Convert ID to string
                additional_claims={
                    'username': user.username,
                    'roles': user.roles
                }
            )
            
            response = jsonify({
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'roles': user.roles
                }
            })
            
            # Set cookies for enhanced security (optional, frontend can also store in memory)
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            
            return response
            
        return jsonify({'error': 'Invalid username or password'}), 401
        
    except Exception as e:
        current_app.logger.error(f'Login error: {str(e)}')
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/api/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        jwt = get_jwt()
        
        # Check if token is in blocklist
        token_id = jwt.get('jti')
        if token_id in token_blocklist:
            return jsonify({'error': 'Token has been revoked'}), 401
            
        user = User.query.get(int(current_user_id))  # Convert string ID back to int
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        access_token = create_access_token(
            identity=str(user.id),  # Convert ID to string
            additional_claims={
                'username': user.username,
                'roles': user.roles
            }
        )
        
        response = jsonify({
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'roles': user.roles
            }
        })
        
        set_access_cookies(response, access_token)
        return response
        
    except Exception as e:
        current_app.logger.error(f'Token refresh error: {str(e)}')
        return jsonify({'error': 'Token refresh failed'}), 500

@auth_bp.route('/api/auth/logout', methods=['POST'])
@jwt_required(verify_type=False)
def logout():
    try:
        # Add token to blocklist
        jwt = get_jwt()
        token_id = jwt.get('jti')
        token_blocklist.add(token_id)
        
        response = jsonify({'message': 'Successfully logged out'})
        unset_jwt_cookies(response)
        return response
    except Exception as e:
        current_app.logger.error(f'Logout error: {str(e)}')
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/api/auth/me', methods=['GET'])
@jwt_required()
def me():
    try:
        current_user_id = get_jwt_identity()
        jwt = get_jwt()
        
        # Check if token is in blocklist
        token_id = jwt.get('jti')
        if token_id in token_blocklist:
            return jsonify({'error': 'Token has been revoked'}), 401
            
        user = User.query.get(int(current_user_id))  # Convert string ID back to int
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({
            'id': user.id,
            'username': user.username,
            'roles': user.roles
        })
    except Exception as e:
        current_app.logger.error(f'User info error: {str(e)}')
        return jsonify({'error': 'Failed to get user info'}), 500

@auth_bp.route('/api/auth/change-password', methods=['POST'])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        jwt = get_jwt()
        
        # Check if token is in blocklist
        token_id = jwt.get('jti')
        if token_id in token_blocklist:
            return jsonify({'error': 'Token has been revoked'}), 401
            
        data = request.get_json()
        if not data or not data.get('current_password') or not data.get('new_password'):
            return jsonify({'error': 'Current password and new password are required'}), 400
            
        user = User.query.get(int(current_user_id))  # Convert string ID back to int
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 401
            
        # Validate new password
        if len(data['new_password']) < 8:
            return jsonify({'error': 'New password must be at least 8 characters long'}), 400
            
        user.set_password(data['new_password'])
        db.session.commit()
        
        # Invalidate all existing tokens
        token_blocklist.add(token_id)
        
        return jsonify({'message': 'Password changed successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Password change error: {str(e)}')
        return jsonify({'error': 'Failed to change password'}), 500

# JWT token callbacks
@jwt_required(verify_type=False)
@auth_bp.route('/api/auth/validate', methods=['POST'])
def validate_token():
    try:
        jwt = get_jwt()
        token_id = jwt.get('jti')
        
        if token_id in token_blocklist:
            return jsonify({'valid': False, 'error': 'Token has been revoked'}), 401
            
        return jsonify({'valid': True}), 200
    except Exception as e:
        return jsonify({'valid': False, 'error': str(e)}), 401 