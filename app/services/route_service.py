from typing import Dict, List, Tuple, Any
import datetime
import os
from importlib.metadata import distributions
from flask import request, jsonify, current_app
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
                api_key = request.headers.get("x-api-key")
                if not api_key or api_key != current_app.config.get("API_KEY"):
                    return jsonify({"error": "Authentication required"}), 401
            return f(*args, **kwargs)

        return decorated_function

    # Custom libs shown first in "Show Versions" (lowercase for matching)
    CUSTOM_LIB_ORDER = ["toloka2mediaserver", "toloka2python", "stream2mediaserver"]

    @classmethod
    def get_installed_packages(cls) -> List[Dict[str, str]]:
        """Get list of installed Python packages and their versions.
        Custom libs are listed first, then the rest alphabetically.
        Returns a list of {name, version} to preserve order in JSON.
        """
        all_packages = {dist.metadata["Name"]: dist.version for dist in distributions()}
        custom_libs = {}
        rest = {}
        for name, version in all_packages.items():
            if name.lower() in cls.CUSTOM_LIB_ORDER:
                custom_libs[name] = version
            else:
                rest[name] = version
        result: List[Dict[str, str]] = []
        for preferred in cls.CUSTOM_LIB_ORDER:
            for name, version in custom_libs.items():
                if name.lower() == preferred:
                    result.append({"name": name, "version": version})
                    break
        for name in sorted(rest.keys(), key=str.lower):
            result.append({"name": name, "version": rest[name]})
        return result

    @classmethod
    def list_files(cls, path: str) -> Tuple[Dict[str, Any], int]:
        """List files in a directory with their details."""
        if not os.path.isdir(path):
            return {"error": "Invalid directory path"}, 400

        try:
            files = []
            for filename in os.listdir(path):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    file_info = os.stat(file_path)
                    files.append(
                        {
                            "name": filename,
                            "size_mb": round(file_info.st_size / (1024 * 1024), 2),
                            "last_modified": datetime.datetime.fromtimestamp(
                                file_info.st_mtime
                            ).strftime("%Y-%m-%d %H:%M:%S"),
                        }
                    )
            return {"files": files}, 200
        except Exception as e:
            return {"error": str(e)}, 500
