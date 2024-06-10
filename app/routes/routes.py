# routes.py

from flask import request, render_template

from ..services import (
    proxy_image_logic
)

def configure_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    @app.route('/image/')
    def proxy_image():
        url = request.args.get('url')
        return proxy_image_logic(url)