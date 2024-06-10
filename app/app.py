# app.py

from flask import Flask
from .routes.routes import configure_routes
from .routes.anime import anime_bp
from .routes.release import release_bp
from .routes.stream import stream_bp
from .routes.studio import studio_bp
from .routes.toloka import toloka_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Set this to a strong secret value
    
    
    app.register_blueprint(anime_bp)
    app.register_blueprint(release_bp)
    app.register_blueprint(stream_bp)
    app.register_blueprint(studio_bp)
    app.register_blueprint(toloka_bp)
    configure_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)