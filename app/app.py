from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_principal import Principal, Permission, RoleNeed
from flask_bcrypt import Bcrypt
import os

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'toloka2web.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

    from .models import user    
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    with app.app_context():
        db.create_all()

    login_manager = LoginManager(app)
    login_manager.login_view = 'login'
    principals = Principal(app)

    admin_permission = Permission(RoleNeed('admin'))
    user_permission = Permission(RoleNeed('user'))

    from .routes.routes import configure_routes
    from .routes.anime import anime_bp
    from .routes.release import release_bp
    from .routes.stream import stream_bp
    from .routes.studio import studio_bp
    from .routes.toloka import toloka_bp

    app.register_blueprint(anime_bp)
    app.register_blueprint(release_bp)
    app.register_blueprint(stream_bp)
    app.register_blueprint(studio_bp)
    app.register_blueprint(toloka_bp)

    configure_routes(app, login_manager)

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)