from flask import Flask
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_bcrypt import Bcrypt
import os

from app.services.config_service import ConfigService
from app.services.services_db import DatabaseService
from .models.base import db
from .models.user import bcrypt

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config is None:
        # Load the default configuration
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'default_secret_key'),
            SQLALCHEMY_DATABASE_URI=f'sqlite:///{os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "toloka2web.db")}',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE='Lax'
        )
    else:
        # Load the test config if passed in
        app.config.update(test_config)

    # Ensure the instance folder exists
    try:
        os.makedirs(os.path.join(app.instance_path, 'data'), exist_ok=True)
    except OSError:
        pass

    # Initialize Flask extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Initialize login manager
    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # Initialize Principal for role-based access control
    principals = Principal(app)
    admin_permission = Permission(RoleNeed('admin'))
    user_permission = Permission(RoleNeed('user'))

    with app.app_context():
        # Import models here to avoid circular imports
        from .models.user import User
        from .models.user_settings import UserSettings
        from .models.releases import Releases
        from .models.application_settings import ApplicationSettings

        # Create database tables
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
    from .routes.anime import anime_bp
    from .routes.release import release_bp
    from .routes.stream import stream_bp
    from .routes.studio import studio_bp
    from .routes.toloka import toloka_bp
    from .routes.mal import mal_bp
    from .routes.tmdb import tmdb_bp
    from .routes.settings import setting_bp
    
    blueprints = [
        anime_bp, release_bp, stream_bp, studio_bp,
        toloka_bp, mal_bp, tmdb_bp, setting_bp
    ]
    
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    # Configure main routes
    configure_routes(app, login_manager, admin_permission, user_permission)

    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)