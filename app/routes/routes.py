# routes.py

from flask import Response, current_app, flash, redirect, request, render_template, url_for, get_flashed_messages, make_response, jsonify
from flask_login import current_user, login_required, login_user, logout_user
from flask_principal import Permission, UserNeed, RoleNeed, identity_changed, Identity, AnonymousIdentity, identity_loaded
from flask_cors import CORS
import os
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.routes.auth import token_blocklist, check_auth

from app.models.application_settings import ApplicationSettings
from app.models.login_form import LoginForm
from app.models.registration_form import RegistrationForm
from app.models.user import User
from app.models.base import db 

from app.services.services import SearchService, TolokaService

def configure_routes(app, login_manager, admin_permission, user_permission):
    # Configure CORS
    CORS(app, resources={
        r"/*": {
            "origins": app.config['CORS_ORIGINS'],
            "supports_credentials": True,
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })

    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.route('/settings')
    @admin_permission.require(http_exception=403)
    def settings():
        return render_template('settings.html')

    @app.route('/image/')
    def proxy_image():
        try:
            url = request.args.get('url')
            if not url:
                return make_response(jsonify({"error": "URL parameter is required"}), 400)
            result = TolokaService.proxy_image_logic(url)
            return make_response(result, 200)
        except Exception as e:
            error_message = {
                "error": "Failed to proxy image",
                "details": str(e)
            }
            return make_response(jsonify(error_message), 500)
    
    @app.route('/api/search')
    @login_required
    def search_aggregated():
        try:
            query = request.args.get('query')
            if not query:
                return make_response(jsonify({"error": "Query parameter is required"}), 400)
            result = SearchService.multi_search(query)
            return make_response(jsonify(result), 200)
        except Exception as e:
            error_message = {
                "error": "Failed to perform search",
                "details": str(e)
            }
            return make_response(jsonify(error_message), 500)

    @app.route('/api/auth/check')
    def check_auth_route():
        result = check_auth()
        if isinstance(result, tuple):
            return make_response(jsonify(result[0]), result[1])
        return make_response(jsonify(result), 200)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        try:
            # For API requests, handle form data differently
            if request.headers.get('Accept') == 'application/json':
                username = request.form.get('username')
                password = request.form.get('password')
                remember = request.form.get('remember_me', 'false').lower() == 'true'

                if not username or not password:
                    return jsonify({'error': 'Username and password are required'}), 400

                user = User.query.filter_by(username=username).first()
                
                if user and user.check_password(password):
                    login_user(user, remember=remember)
                    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                    
                    return jsonify({
                        'id': user.id,
                        'username': user.username,
                        'roles': user.roles
                    })
                else:
                    return jsonify({'error': 'Invalid username or password'}), 401

            # For regular form submissions
            form = LoginForm()
            if form.validate_on_submit():
                username = form.username.data
                password = form.password.data
                remember = form.remember_me.data
                user = User.query.filter_by(username=username).first()
                
                if user and user.check_password(password):
                    login_user(user, remember=remember)
                    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'error')
            
            return render_template('login.html', form=form)
        except Exception as e:
            app.logger.error(f'Login error: {str(e)}')
            error_message = 'Login failed due to an unexpected error'
            if request.headers.get('Accept') == 'application/json':
                return jsonify({'error': error_message}), 500
            
            flash(error_message, 'error')
            return render_template('login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        try:
            form = RegistrationForm()
            open_registration = ApplicationSettings.query.filter_by(key='open_registration').first()
            
            if not getattr(open_registration, 'value', None) or open_registration.value.lower() != 'true':
                flash('Registration is closed or not set.', 'error')
                return render_template('register.html', form=form)

            if form.validate_on_submit():
                user = User(username=form.username.data)
                user.set_password(form.password.data)
                # Check if this is the first user
                user.roles = 'admin' if User.query.count() == 0 else 'user'
                
                db.session.add(user)
                db.session.commit()
                flash('Account registered', 'info')
                return redirect(url_for('login'))
                
            return render_template('register.html', form=form)
        except Exception as e:
            flash('Registration failed due to an unexpected error', 'error')
            return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required 
    def logout():
        try:
            logout_user()
            identity_changed.send(app, identity=AnonymousIdentity()) 
            flash('You have been logged out.', 'info')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Logout failed due to an unexpected error', 'error')
            return redirect(url_for('index'))

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        identity.user = current_user
    
        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))
    
        # Assuming the User model has a list of roles, update the identity with the roles that the user provides
        if hasattr(current_user, 'roles'):
            identity.provides.add(RoleNeed(current_user.roles))
    
    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            identity_changed.send(current_app._get_current_object(), identity=Identity(current_user.id))
            
    @app.route('/static/js/common/user.js')
    def user_script():
        try:
            if current_user.is_authenticated:
                user_id = current_user.id if current_user.id else "undefined"
                user_roles = current_user.roles if current_user.roles else ""
            else:
                user_id = "undefined"
                user_roles = ""
        
            js_content = f"""
            const user = {{
                id: "{user_id}",
                roles: "{user_roles}"
            }};
            export default user;
            """
        
            return Response(js_content, mimetype='application/javascript')
        except Exception as e:
            error_message = "Failed to generate user script"
            return Response(f"console.error('{error_message}')", mimetype='application/javascript', status=500)