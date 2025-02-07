from typing import Dict
import requests
from app.models.application_settings import ApplicationSettings
from app.models.base import db

from app.services.base_service import BaseService

class TMDBService(BaseService):
    """Service for interacting with The Movie Database (TMDB) API."""
    
    API_BASE_URL = "https://api.themoviedb.org/3"
    
    @classmethod
    def search_media(cls, query: str, language: str = 'uk-UK') -> Dict:
        """Search for media (movies, TV shows, etc.) using TMDB API."""
        api_key = cls.get_api_key('tmdb_api')
        if not api_key:
            return {'error': 'TMDB API key not found'}
            
        url = f"{cls.API_BASE_URL}/search/multi"
        params = {
            'api_key': api_key,
            'query': query,
            'include_adult': True,
            'language': language
        }
        
        response = requests.get(url, params=params)
        return cls.handle_api_response(response, "TMDB API Error")

    @classmethod
    def get_media_detail(cls, media_id: int, media_type: str = 'tv', language: str = 'uk-UK') -> Dict:
        """Get detailed information about a specific media item."""
        api_key = cls.get_api_key('tmdb_api')
        if not api_key:
            return {'error': 'TMDB API key not found'}
            
        url = f"{cls.API_BASE_URL}/{media_type}/{media_id}"
        params = {
            'api_key': api_key,
            'append_to_response': 'external_ids,images,alternative_titles',
            'language': language
        }
        
        response = requests.get(url, params=params)
        return cls.handle_api_response(response, "TMDB API Error")

    @classmethod
    def get_by_external_id(cls, external_id: str, source: str) -> Dict:
        """Find TMDB content using external IDs (IMDB, TVDB)."""
        api_key = cls.get_api_key('tmdb_api')
        if not api_key:
            return {'error': 'TMDB API key not found'}
            
        url = f"{cls.API_BASE_URL}/find/{external_id}"
        params = {
            'api_key': api_key,
            'external_source': source
        }
        
        response = requests.get(url, params=params)
        return cls.handle_api_response(response, "TMDB API Error")

    @classmethod
    def get_trending_by_type(cls, media_type: str = 'tv', language: str = 'uk-UK') -> Dict:
        """Get trending content by media type."""
        api_key = cls.get_api_key('tmdb_api')
        if not api_key:
            return {'error': 'TMDB API key not found'}
            
        url = f"{cls.API_BASE_URL}/trending/{media_type}/day"
        params = {
            'api_key': api_key,
            'language': language
        }
        
        response = requests.get(url, params=params)
        return cls.handle_api_response(response, "TMDB API Error")

def get_api_key(key_name):
    setting = ApplicationSettings.query.filter_by(key=key_name).first()
    return setting.value if setting else None