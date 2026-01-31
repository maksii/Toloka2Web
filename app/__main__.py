# app/__main__.py
"""
Module entry point for Toloka2Web application.

Usage:
    python -m app

This is an alternative to running `python run.py`.
Both methods are equivalent - create_app() handles all initialization.
"""


def main():
    """Main entry point for module execution."""
    from .app import create_app

    # Create and configure the application
    # create_app() handles all initialization including:
    # - Data file downloads (anime_data.db, app.ini, titles.ini)
    # - Database initialization
    # - Extension setup
    app = create_app()

    # Get host and port from config
    port = app.config.get("PORT", 5000)
    host = app.config.get("HOST", "0.0.0.0")

    # Run the Flask application
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()
