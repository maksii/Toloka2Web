import requests
from app.models.application_settings import ApplicationSettings
from app.models.base import db

def get_api_key(key_name):
    setting = ApplicationSettings.query.filter_by(key=key_name).first()
    return setting.value if setting else None

def search_anime(query):
    api_key = get_api_key('mal_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.myanimelist.net/v2/anime?q={query}"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_anime_detail(anime_id):
    api_key = get_api_key('mal_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}"
    headers = {'Authorization': f'Bearer {api_key}'}
    response = requests.get(url, headers=headers)
    return response.json()