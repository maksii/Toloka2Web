"""MAL (MyAnimeList) API service."""

from typing import Dict
import requests

from app.services.base_service import BaseService


class MALService(BaseService):
    """Service for interacting with MyAnimeList API."""

    API_BASE_URL = "https://api.myanimelist.net/v2"

    @classmethod
    def search_anime(cls, query: str) -> Dict:
        """Search for anime using MAL API."""
        api_key = cls.get_api_key("mal_api")
        if not api_key:
            return {"error": "MAL API key not found"}

        url = f"{cls.API_BASE_URL}/anime"
        params = {
            "q": query,
            "limit": 10,
            "fields": "id,title,main_picture,alternative_titles,media_type,status,start_date,end_date",
        }
        headers = {"X-MAL-CLIENT-ID": api_key}

        response = requests.get(url, params=params, headers=headers, timeout=30)
        return cls.handle_api_response(response, "MAL API Error")

    @classmethod
    def get_anime_detail(cls, anime_id: int) -> Dict:
        """Get detailed information about a specific anime."""
        api_key = cls.get_api_key("mal_api")
        if not api_key:
            return {"error": "MAL API key not found"}

        url = f"{cls.API_BASE_URL}/anime/{anime_id}"
        params = {
            "fields": "id,title,main_picture,alternative_titles,start_date,end_date,synopsis,rank,"
            "popularity,status,num_episodes,rating,pictures,background,related_anime"
        }
        headers = {"X-MAL-CLIENT-ID": api_key}

        response = requests.get(url, params=params, headers=headers, timeout=30)
        return cls.handle_api_response(response, "MAL API Error")
