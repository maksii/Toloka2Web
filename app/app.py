# app.py

from flask import Flask
from .routes import configure_routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # Set this to a strong secret value
    configure_routes(app)
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)