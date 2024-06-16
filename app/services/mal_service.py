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
    url = f"https://api.myanimelist.net/v2/anime?q={query}&limit=10&fields=id,title,main_picture,alternative_titles,media_type,status,start_date,end_date"
    headers = {'X-MAL-CLIENT-ID': f'{api_key}'}
    response = requests.get(url, headers=headers)
    return response.json()

def get_anime_detail(anime_id):
    api_key = get_api_key('mal_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.myanimelist.net/v2/anime/{anime_id}?fields=id,title,main_picture,alternative_titles,start_date,end_date,synopsis,rank,popularity,status,num_episodes,rating,pictures,background,related_anime"
    headers = {'X-MAL-CLIENT-ID': f'{api_key}'}
    response = requests.get(url, headers=headers)
    return response.json()