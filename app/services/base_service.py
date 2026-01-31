from typing import Any, Dict, Optional
from app.models.application_settings import ApplicationSettings

class BaseService:
    """Base class for all services providing common functionality."""
    
    @classmethod
    def get_api_key(cls, key_name: str) -> Optional[str]:
        """Get API key from application settings."""
        setting = ApplicationSettings.query.filter_by(key=key_name).first()
        return setting.value if setting else None

    @classmethod
    def serialize(cls, data: Any) -> Any:
        """Serialize SQLAlchemy objects to JSON-compatible format."""
        if isinstance(data, list):
            return [cls.serialize(item) for item in data]
        elif hasattr(data, '__dict__'):
            result = {}
            for column in data.__dict__:
                if not column.startswith('_'):
                    attr = getattr(data, column)
                    if hasattr(attr, '__dict__') or isinstance(attr, list):
                        result[column] = cls.serialize(attr)
                    else:
                        result[column] = attr
            return result
        return data

    @classmethod
    def handle_api_response(cls, response: Any, error_msg: str = "API Error") -> Dict:
        """Handle API response and standardize error format."""
        try:
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {'error': f"{error_msg}: {str(e)}"} 