import requests
from app.models.application_settings import ApplicationSettings
from app.models.base import db

def get_api_key(key_name):
    setting = ApplicationSettings.query.filter_by(key=key_name).first()
    return setting.value if setting else None

def search_media(query, language = 'uk-UK'):
    api_key = get_api_key('tmdb_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.themoviedb.org/3/search/multi?api_key={api_key}&query={query}&include_adult=true&language={language}"
    response = requests.get(url)
    return response.json()

def get_media_detail(id, type = 'tv', language = 'uk-UK'):
    api_key = get_api_key('tmdb_api')
    if not api_key:
        return {'error': 'API key not found'}
    
    url = f"https://api.themoviedb.org/3/{type}/{id}?api_key={api_key}&append_to_response=external_ids%2Cimages%2Calternative_titles&language={language}"
    
    response = requests.get(url)
    return response.json()

def get_by_external_id(id, source):
    #source=imdb_id
    #source=tvdb_id
    api_key = get_api_key('tmdb_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.themoviedb.org/3/find/{id}?api_key={api_key}&external_source={source}"
    response = requests.get(url)
    return response.json()

def get_trending_by_type(type = 'tv', language = 'uk-UK'):
    api_key = get_api_key('tmdb_api')
    if not api_key:
        return {'error': 'API key not found'}
    
    url = f"https://api.themoviedb.org/3/trending/{type}/day?api_key={api_key}&language={language}"
    
    response = requests.get(url)
    return response.json()