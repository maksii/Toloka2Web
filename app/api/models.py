from flask_restx import fields
from . import api

# Common Models
error_response = api.model('ErrorResponse', {
    'error': fields.String(description='Error message'),
    'code': fields.String(description='Error code', required=False),
    'details': fields.String(description='Error details', required=False)
})

success_response = api.model('SuccessResponse', {
    'message': fields.String(description='Success message')
})

# Auth Models
login_model = api.model('Login', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password'),
    'remember_me': fields.Boolean(required=False, description='Remember me flag')
})

register_model = api.model('Register', {
    'username': fields.String(required=True, description='User username'),
    'password': fields.String(required=True, description='User password')
})

user_info = api.model('UserInfo', {
    'id': fields.Integer(description='User ID'),
    'username': fields.String(description='Username'),
    'roles': fields.String(description='User roles')
})

token_response = api.model('TokenResponse', {
    'access_token': fields.String(description='JWT access token'),
    'refresh_token': fields.String(description='JWT refresh token'),
    'user': fields.Nested(user_info)
})

# Anime Models
anime_model = api.model('Anime', {
    'id': fields.Integer(description='Anime ID'),
    'name': fields.String(description='Anime name'),
    'description': fields.String(description='Anime description'),
    'studio_id': fields.Integer(description='Studio ID'),
    'mal_id': fields.Integer(description='MyAnimeList ID'),
    'tmdb_id': fields.Integer(description='TMDB ID')
})

# Studio Models
studio_model = api.model('Studio', {
    'id': fields.Integer(description='Studio ID'),
    'name': fields.String(description='Studio name'),
    'description': fields.String(description='Studio description')
})

# Search Models
search_input = api.model('SearchInput', {
    'query': fields.String(required=True, description='Search query')
})

search_response = api.model('SearchResponse', {
    'anime': fields.List(fields.Nested(anime_model)),
    'studios': fields.List(fields.Nested(studio_model))
})

# Release Models
release_input = api.model('ReleaseInput', {
    'codename': fields.String(required=True, description='Release codename'),
    'title': fields.String(required=True, description='Release title'),
    'description': fields.String(description='Release description'),
    'status': fields.String(description='Release status'),
    'type': fields.String(description='Release type'),
    'season': fields.String(description='Release season'),
    'year': fields.Integer(description='Release year')
})

release_output = api.model('ReleaseOutput', {
    'id': fields.Integer(description='Release ID'),
    'codename': fields.String(description='Release codename'),
    'title': fields.String(description='Release title'),
    'description': fields.String(description='Release description'),
    'status': fields.String(description='Release status'),
    'type': fields.String(description='Release type'),
    'season': fields.String(description='Release season'),
    'year': fields.Integer(description='Release year'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

# Settings Models
setting_model = api.model('Setting', {
    'section': fields.String(required=True, description='Setting section'),
    'key': fields.String(required=True, description='Setting key'),
    'value': fields.String(required=True, description='Setting value')
})

# Torrent Models
torrent_info = api.model('TorrentInfo', {
    'name': fields.String(description='Torrent name'),
    'size': fields.String(description='Torrent size'),
    'seeders': fields.Integer(description='Number of seeders'),
    'leechers': fields.Integer(description='Number of leechers'),
    'uploaded_at': fields.DateTime(description='Upload timestamp')
})

# Common response wrappers
def with_pagination(model):
    """Wrap a model with pagination fields"""
    return api.model(f'Paginated{model.name}', {
        'items': fields.List(fields.Nested(model)),
        'total': fields.Integer(description='Total number of items'),
        'page': fields.Integer(description='Current page number'),
        'per_page': fields.Integer(description='Items per page'),
        'pages': fields.Integer(description='Total number of pages')
    })

# Standard response codes
responses = {
    200: 'Success',
    201: 'Created',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Internal Server Error'
}

# Collection Response Models
anime_list_response = api.model('AnimeListResponse', {
    'data': fields.List(fields.Nested(anime_model))
})

studio_list_response = api.model('StudioListResponse', {
    'data': fields.List(fields.Nested(studio_model))
})

user_list_response = api.model('UserListResponse', {
    'data': fields.List(fields.Nested(user_info))
})

settings_list_response = api.model('SettingsListResponse', {
    'data': fields.List(fields.Nested(setting_model))
})

mal_search_response = api.model('MALSearchResponse', {
    'data': fields.List(fields.Raw(description='MAL search results'))
})

tmdb_search_response = api.model('TMDBSearchResponse', {
    'data': fields.List(fields.Raw(description='TMDB search results'))
}) 