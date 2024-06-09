# app/__main__.py

import os
from .app import create_app

app = create_app()

if __name__ == '__main__':
    # Set the default port to 5000 if not specified
    port = int(os.getenv('PORT', 5000))
    # Set the default host to '0.0.0.0' to run on all network interfaces
    host = os.getenv('HOST', '0.0.0.0')

    # Run the Flask application with the specified host and port
    app.run(host=host, port=port)