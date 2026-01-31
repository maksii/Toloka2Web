# app/__init__.py
"""
Toloka2Web Application Package.

This package provides a web interface for managing anime content,
with features for searching, downloading, and organizing media from various sources.
"""

from .app import create_app

__all__ = ["create_app"]
