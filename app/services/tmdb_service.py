import requests
from app.models.application_settings import ApplicationSettings
from app.models.base import db

def get_api_key(key_name):
    setting = ApplicationSettings.query.filter_by(key=key_name).first()
    return setting.value if setting else None

def search_movie(query):
    api_key = get_api_key('tmdb_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
    response = requests.get(url)
    return response.json()

def get_movie_detail(movie_id):
    api_key = get_api_key('tmdb_api')
    if not api_key:
        return {'error': 'API key not found'}
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}"
    response = requests.get(url)
    return response.json()