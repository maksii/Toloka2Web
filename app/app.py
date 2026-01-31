# Standard library imports
from datetime import timedelta
import os
import sqlite3
import logging

# Third-party imports
import requests

# Flask and extensions
from flask import Flask, jsonify
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_jwt_extended import JWTManager

# Local imports
from app.services.config_service import ConfigService
from app.services.services_db import DatabaseService
from .models.base import db
from .models.user import bcrypt

# Default secret values that should not be used in production
_DEFAULT_SECRETS = {
    'FLASK_SECRET_KEY': 'default_secret_key',
    'JWT_SECRET_KEY': 'default_jwt_secret',
    'API_KEY': 'default_api_key',
}


def _initialize_data_files():
    """Initialize required data files before app startup.
    
    Creates necessary directories and downloads required files if they don't exist:
    - data/anime_data.db: Anime database (downloaded if missing)
    - data/app.ini: Application configuration (downloaded if missing)
    - data/titles.ini: Release tracking (created empty if missing)
    
    This function is called during create_app() to ensure all required
    files exist before the Flask application is fully initialized.
    """
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Check and download anime database if not exists
    local_db_path = "data/anime_data.db"
    if not os.path.exists(local_db_path):
        logging.info("Database not found. Downloading the database...")
        try:
            DatabaseService.update_database()
        except Exception as e:
            logging.warning(f"Failed to download anime database: {e}")
    
    # Check and download app.ini if not exists
    app_ini_path = "data/app.ini"
    if not os.path.exists(app_ini_path):
        logging.info("app.ini not found. Downloading template...")
        try:
            response = requests.get(
                "https://raw.githubusercontent.com/CakesTwix/Toloka2MediaServer/main/data/app-example.ini",
                timeout=30
            )
            response.raise_for_status()
            with open(app_ini_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Downloaded app.ini to {app_ini_path}")
        except Exception as e:
            logging.warning(f"Failed to download app.ini: {e}")
    
    # Check and create titles.ini if not exists
    titles_ini_path = "data/titles.ini"
    if not os.path.exists(titles_ini_path):
        logging.info("titles.ini not found. Creating empty file...")
        try:
            with open(titles_ini_path, 'w', encoding='utf-8') as f:
                pass  # Create empty file
        except OSError as e:
            logging.warning(f"Failed to create titles.ini: {e}")


def _validate_environment_config(app):
    """Validate environment configuration and log warnings for insecure defaults.
    
    This function checks if the application is using default secret values
    and logs appropriate warnings. In production, these should be set to
    secure random values.
    """
    warnings = []
    
    if app.config.get('SECRET_KEY') == _DEFAULT_SECRETS['FLASK_SECRET_KEY']:
        warnings.append(
            "FLASK_SECRET_KEY is using default value. "
            "Set FLASK_SECRET_KEY environment variable for production."
        )
    
    if app.config.get('JWT_SECRET_KEY') == _DEFAULT_SECRETS['JWT_SECRET_KEY']:
        warnings.append(
            "JWT_SECRET_KEY is using default value. "
            "Set JWT_SECRET_KEY environment variable for production."
        )
    
    if app.config.get('API_KEY') == _DEFAULT_SECRETS['API_KEY']:
        warnings.append(
            "API_KEY is using default value. "
            "Set API_KEY environment variable for production."
        )
    
    for warning in warnings:
        app.logger.warning(f"SECURITY WARNING: {warning}")


def run_database_migrations(app):
    """Run database migrations for schema changes.
    
    This function handles adding new columns to existing tables
    that db.create_all() cannot handle for existing databases.
    """
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        # Database doesn't exist yet, no migration needed
        return
    
    migrations = [
        # Migration: Add 'ongoing' column to releases table
        {
            'table': 'releases',
            'column': 'ongoing',
            'sql': "ALTER TABLE releases ADD COLUMN ongoing BOOLEAN DEFAULT 1 NOT NULL"
        },
    ]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        for migration in migrations:
            # Check if column exists
            cursor.execute(f"PRAGMA table_info({migration['table']})")
            columns = [info[1] for info in cursor.fetchall()]
            
            if migration['column'] not in columns:
                try:
                    cursor.execute(migration['sql'])
                    conn.commit()
                    app.logger.info(f"Migration: Added '{migration['column']}' column to '{migration['table']}' table")
                except sqlite3.Error as e:
                    app.logger.warning(f"Migration warning for {migration['column']}: {e}")
        
        conn.close()
    except sqlite3.Error as e:
        app.logger.error(f"Database migration error: {e}")

def create_app(test_config=None):
    """Create and configure the Flask application.
    
    Args:
        test_config: Optional configuration dictionary for testing.
        
    Returns:
        Configured Flask application instance.
    """
    # Initialize data files before creating app (downloads if missing)
    if test_config is None:
        _initialize_data_files()
    
    app = Flask(__name__)
    
    if test_config is None:
        # Load the default configuration
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'default_secret_key'),
            SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "toloka2web.db")}',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SESSION_COOKIE_SECURE=False,  # Changed from True to allow both HTTP and HTTPS
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='Lax',
            SESSION_COOKIE_DOMAIN=None,  # Allow cookies to work across different IPs
            # CSRF Configuration
            WTF_CSRF_TIME_LIMIT=3600,  # 1 hour CSRF token validity
            WTF_CSRF_SSL_STRICT=False,  # Allow CSRF token to work across HTTP/HTTPS
            WTF_CSRF_CHECK_DEFAULT=False,  # Don't enforce referrer checking (allows different hostnames/IPs)
            # JWT Configuration
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY', 'default_jwt_secret'),  # Change this in production!
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=24),
            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
            JWT_COOKIE_SECURE=False,  # Changed from True to allow both HTTP and HTTPS
            JWT_COOKIE_CSRF_PROTECT=True,
            JWT_COOKIE_SAMESITE='Lax',
            JWT_ERROR_MESSAGE_KEY='error',
            # API Key Configuration
            API_KEY=os.environ.get('API_KEY', 'default_api_key'),  # Change this in production!
            # Server Configuration
            PORT=int(os.environ.get('PORT', 5000)),
            HOST=os.environ.get('HOST', '0.0.0.0'),
            # CORS Configuration
            CORS_ORIGINS=os.environ.get('CORS_ORIGINS', '*').split(',')
        )
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Validate environment configuration (warn about insecure defaults)
    _validate_environment_config(app)

    # Ensure the instance folder exists
    try:
        os.makedirs(os.path.join(app.instance_path, 'data'), exist_ok=True)
    except OSError:
        pass

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt = JWTManager(app)

    # JWT error handlers
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has expired',
            'code': 'token_expired'
        }), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid token',
            'code': 'invalid_token'
        }), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization token is missing',
            'code': 'authorization_required'
        }), 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Fresh token required',
            'code': 'fresh_token_required'
        }), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token has been revoked',
            'code': 'token_revoked'
        }), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        """Check if a JWT token has been revoked.
        
        Checks both the in-memory blocklist (for immediate revocation)
        and the database (for persistence across restarts).
        """
        from .routes.auth import token_blocklist
        from .models.revoked_token import RevokedToken
        
        jti = jwt_payload["jti"]
        # Check in-memory first (faster), then database
        return jti in token_blocklist or RevokedToken.is_token_revoked(jti)

    # Initialize login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Initialize Principal for role-based access control
    Principal(app)
    admin_permission = Permission(RoleNeed('admin'))
    user_permission = Permission(RoleNeed('user'))

    # Configure logging
    from .utils.logging_config import configure_logging
    configure_logging(app)

    # Register error handlers for consistent API error responses
    from .utils.errors import register_error_handlers
    register_error_handlers(app)

    # Run database migrations before creating tables
    run_database_migrations(app)
    
    with app.app_context():
        # Import models here to avoid circular imports
        from .models.releases import Releases
        from .models.application_settings import ApplicationSettings

        # Create database tables (including revoked_tokens for JWT blocklist)
        db.create_all()
        DatabaseService.initialize_database()

        # Initialize application settings if needed
        if not ApplicationSettings.query.first():
            app_config_path = 'data/app.ini'
            ConfigService.read_settings_ini_and_sync_to_db(app_config_path)
            ConfigService.init_web_settings()

        # Initialize releases if needed
        if not Releases.query.first():
            title_config_path = 'data/titles.ini'
            ConfigService.read_releases_ini_and_sync_to_db(title_config_path)

    # Register blueprints
    from .routes.routes import configure_routes
    from .routes.anime import anime_bp, anime_api_bp
    from .routes.release import release_bp
    from .routes.stream import stream_bp
    from .routes.studio import studio_bp, studio_api_bp
    from .routes.toloka import toloka_bp
    from .routes.mal import mal_bp
    from .routes.tmdb import tmdb_bp
    from .routes.settings import setting_bp
    from .routes.auth import auth_bp
    from .routes.users import user_bp
    from .api import api_bp  # Import the API blueprint
    
    # Register blueprints with URL prefixes
    app.register_blueprint(api_bp)  # api_bp already has url_prefix='/api'
    
    # Define which blueprints should be registered with API prefix
    api_blueprints = [
        anime_api_bp, studio_api_bp, release_bp, stream_bp,
        toloka_bp, mal_bp, tmdb_bp, setting_bp, auth_bp,
        user_bp
    ]
    
    # Define blueprints that should be registered without API prefix (HTML pages)
    html_blueprints = [
        anime_bp,  # Contains HTML routes for anime pages
        studio_bp,  # Contains HTML routes for studio pages
    ]
    
    # Register API blueprints with '/api' prefix
    for blueprint in api_blueprints:
        app.register_blueprint(blueprint, url_prefix='/api')
    
    # Register HTML blueprints without prefix
    for blueprint in html_blueprints:
        app.register_blueprint(blueprint)

    # Configure main routes that should be registered directly with the app
    configure_routes(app, login_manager, admin_permission, user_permission)

    return app

if __name__ == "__main__":
    app = create_app()
    port = app.config['PORT']
    host = app.config['HOST']
    app.run(host=host, port=port, debug=True)
