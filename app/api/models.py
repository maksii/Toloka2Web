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
torrent_info_model = api.model('TorrentInfo', {
    'state': fields.String(description='Torrent state'),
    'progress': fields.Float(description='Download progress'),
    'name': fields.String(description='Torrent name')
})

release_model = api.model('Release', {
    'hash': fields.String(description='Release hash'),
    'title': fields.String(description='Release title'),
    'torrent_info': fields.Nested(torrent_info_model, description='Torrent information'),
    'status': fields.String(description='Release status'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

releases_list_response = api.model('ReleasesListResponse', {
    'data': fields.List(fields.Nested(release_model)),
    'message': fields.String(description='Response message')
})

release_input = api.model('ReleaseInput', {
    'title': fields.String(required=True, description='Release title'),
    'hash': fields.String(required=True, description='Release hash'),
    'status': fields.String(description='Release status')
})

# Settings Models
setting_model = api.model('Setting', {
    'section': fields.String(required=True, description='Setting section'),
    'key': fields.String(required=True, description='Setting key'),
    'value': fields.String(required=True, description='Setting value')
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

# Stream Models
stream_search_input = api.model('StreamSearchInput', {
    'query': fields.String(required=True, description='Search query')
})

stream_add_input = api.model('StreamAddInput', {
    'provider': fields.String(required=True, description='Streaming provider'),
    'link': fields.String(required=True, description='Title link'),
    'title': fields.String(required=True, description='Title name')
})

stream_details_input = api.model('StreamDetailsInput', {
    'provider': fields.String(required=True, description='Streaming provider'),
    'link': fields.String(required=True, description='Title link')
})

stream_response = api.model('StreamResponse', {
    'data': fields.Raw(description='Stream data'),
    'message': fields.String(description='Response message')
})

# Toloka Models
toloka_torrent_model = api.model('TolokaTorrent', {
    'id': fields.String(description='Torrent ID'),
    'title': fields.String(description='Torrent title'),
    'size': fields.String(description='Torrent size'),
    'seeders': fields.Integer(description='Number of seeders'),
    'leechers': fields.Integer(description='Number of leechers'),
    'hash': fields.String(description='Torrent hash')
})

toloka_search_response = api.model('TolokaSearchResponse', {
    'data': fields.List(fields.Nested(toloka_torrent_model)),
    'message': fields.String(description='Response message')
})

toloka_add_input = api.model('TolokaAddInput', {
    'release_id': fields.String(required=True, description='Release ID'),
    'title': fields.String(required=True, description='Torrent title')
})

# Aggregated Search Models
aggregated_search_response = api.model('AggregatedSearchResponse', {
    'anime': fields.List(fields.Nested(anime_model)),
    'studios': fields.List(fields.Nested(studio_model)),
    'toloka': fields.List(fields.Nested(toloka_torrent_model)),
    'streaming': fields.List(fields.Raw(description='Streaming search results'))
})

# Auth Check Models
auth_check_response = api.model('AuthCheckResponse', {
    'authenticated': fields.Boolean(description='Authentication status'),
    'user': fields.Nested(user_info, description='User information if authenticated')
})

# Image Proxy Models
image_proxy_response = api.model('ImageProxyResponse', {
    'content_type': fields.String(description='Image content type'),
    'data': fields.String(description='Base64 encoded image data')
}) 