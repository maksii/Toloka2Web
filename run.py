#!/usr/bin/env python
"""
Main entry point for Toloka2Web application.

This is the recommended way to run the application:
    python run.py

For module execution, use:
    python -m app
"""

import os
import sys


def main():
    """Run the Toloka2Web application."""
    # Ensure the data directory exists
    os.makedirs('data', exist_ok=True)
    
    # Import and create the app
    from app import create_app
    
    app = create_app()
    
    # Get host and port from config (set from environment variables)
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    
    # Run the application
    app.run(host=host, port=port)


if __name__ == '__main__':
    main()
