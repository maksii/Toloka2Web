from typing import Dict, List, Tuple, Any
import datetime
import os
from importlib.metadata import distributions
from flask import request, jsonify, abort, g, current_app
from flask_login import current_user
from functools import wraps

from app.services.base_service import BaseService

class RouteService(BaseService):
    """Service for handling route-related functionality."""

    @classmethod
    def login_or_api_key_required(cls, f):
        """Decorator to check for valid login or API key."""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                api_key = request.headers.get('x-api-key')
                if not api_key or api_key != current_app.config.get('API_KEY'):
                    return jsonify({"error": "Authentication required"}), 401
            return f(*args, **kwargs)
        return decorated_function

    @classmethod
    def get_installed_packages(cls) -> Dict[str, str]:
        """Get list of installed Python packages and their versions."""
        return {dist.metadata["Name"]: dist.version for dist in distributions()}

    @classmethod
    def list_files(cls, path: str) -> Tuple[Dict[str, Any], int]:
        """List files in a directory with their details."""
        if not os.path.isdir(path):
            return {'error': 'Invalid directory path'}, 400

        try:
            files = []
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    file_info = os.stat(file_path)
                    files.append({
                        'name': filename,
                        'size_mb': round(file_info.st_size / (1024 * 1024), 2),
                        'last_modified': datetime.datetime.fromtimestamp(file_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            return {'files': files}, 200
        except Exception as e:
            return {'error': str(e)}, 500