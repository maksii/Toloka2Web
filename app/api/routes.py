from flask import request, jsonify
from flask_restx import Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.auth_utils import multi_auth_required, multi_auth_admin_required

from . import api, auth_ns, releases_ns, settings_ns, anime_ns, stream_ns, studio_ns, toloka_ns, mal_ns, tmdb_ns, users_ns
from .models import (
    error_response, success_response, login_model, register_model, token_response,
    user_info, anime_model, studio_model, search_input, search_response,
    release_input, release_output, setting_model, torrent_info,
    anime_list_response, studio_list_response, user_list_response,
    settings_list_response, mal_search_response, tmdb_search_response
)

from app.services.services_db import DatabaseService
from app.services.services import SearchService, TolokaService
from app.services.mal_service import MALService
from app.services.tmdb_service import TMDBService
from app.models.user import User
from app.models.application_settings import ApplicationSettings

# Auth Routes
@auth_ns.route('/register')
class Register(Resource):
    @api.doc('register',
        responses={
            201: ('Success', token_response),
            400: ('Bad Request', error_response),
            403: ('Registration Closed', error_response),
            409: ('Username Exists', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.expect(register_model)
    def post(self):
        """Register a new user account"""
        from app.routes.auth import register
        return register()

# Anime Routes
@anime_ns.route('')
class AnimeList(Resource):
    @api.doc('list_anime',
        responses={
            200: ('Success', anime_list_response),
            400: ('Bad Request', error_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.param('query', 'Search query (optional)')
    @multi_auth_required
    def get(self):
        """List all anime or search by name"""
        from app.routes.anime import list_anime
        return list_anime()

@anime_ns.route('/<int:anime_id>')
class AnimeDetail(Resource):
    @api.doc('get_anime',
        responses={
            200: ('Success', anime_model),
            401: ('Unauthorized', error_response),
            404: ('Not Found', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_required
    def get(self, anime_id):
        """Get anime details by ID"""
        from app.routes.anime import get_anime_byid
        return get_anime_byid(anime_id)

# Studio Routes
@studio_ns.route('')
class StudioList(Resource):
    @api.doc('list_studios',
        responses={
            200: ('Success', studio_list_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.param('query', 'Search query (optional)')
    @multi_auth_required
    def get(self):
        """List all studios or search by name"""
        from app.routes.studio import search_studio
        return search_studio()

@studio_ns.route('/<int:studio_id>')
class StudioDetail(Resource):
    @api.doc('get_studio',
        responses={
            200: ('Success', studio_model),
            401: ('Unauthorized', error_response),
            404: ('Not Found', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_required
    def get(self, studio_id):
        """Get studio details by ID"""
        from app.routes.studio import get_studio_details
        return get_studio_details(studio_id)

@studio_ns.route('/<int:studio_id>/anime')
class StudioAnime(Resource):
    @api.doc('list_studio_anime',
        responses={
            200: ('Success', anime_list_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_required
    def get(self, studio_id):
        """List all anime from a specific studio"""
        from app.routes.studio import list_titles_by_studio
        return list_titles_by_studio(studio_id)

# MAL Routes
@mal_ns.route('/search')
class MALSearch(Resource):
    @api.doc('search_mal',
        responses={
            200: ('Success', mal_search_response),
            400: ('Bad Request', error_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.param('query', 'Search query', required=True)
    @multi_auth_required
    def get(self):
        """Search anime on MyAnimeList"""
        from app.routes.mal import search
        return search()

@mal_ns.route('/detail/<int:anime_id>')
class MALDetail(Resource):
    @api.doc('get_mal_detail',
        responses={
            200: ('Success', fields.Raw),
            401: ('Unauthorized', error_response),
            404: ('Not Found', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_required
    def get(self, anime_id):
        """Get anime details from MyAnimeList"""
        from app.routes.mal import get_detail
        return get_detail(anime_id)

# TMDB Routes
@tmdb_ns.route('/search')
class TMDBSearch(Resource):
    @api.doc('search_tmdb',
        responses={
            200: ('Success', tmdb_search_response),
            400: ('Bad Request', error_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.param('query', 'Search query', required=True)
    @multi_auth_required
    def get(self):
        """Search media on TMDB"""
        from app.routes.tmdb import search
        return search()

@tmdb_ns.route('/detail/<int:id>')
class TMDBDetail(Resource):
    @api.doc('get_tmdb_detail',
        responses={
            200: ('Success', fields.Raw),
            400: ('Bad Request', error_response),
            401: ('Unauthorized', error_response),
            404: ('Not Found', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.param('type', 'Media type (movie/tv)', required=True)
    @multi_auth_required
    def get(self, id):
        """Get media details from TMDB"""
        from app.routes.tmdb import get_detail
        return get_detail(id)

# Settings Routes
@settings_ns.route('')
class Settings(Resource):
    @api.doc('list_settings',
        responses={
            200: ('Success', settings_list_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_admin_required
    def get(self):
        """List all application settings"""
        from app.routes.settings import list_setting
        return list_setting()

    @api.doc('add_setting',
        responses={
            200: ('Success', setting_model),
            400: ('Bad Request', error_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.expect(setting_model)
    @multi_auth_admin_required
    def post(self):
        """Add a new application setting"""
        from app.routes.settings import add
        return add()

# User Routes
@users_ns.route('/profile')
class UserProfile(Resource):
    @api.doc('get_profile',
        responses={
            200: ('Success', user_info),
            401: ('Unauthorized', error_response),
            404: ('Not Found', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_required
    def get(self):
        """Get current user's profile"""
        from app.routes.users import get_profile
        return get_profile()

@users_ns.route('')
class UserList(Resource):
    @api.doc('list_users',
        responses={
            200: ('Success', user_list_response),
            401: ('Unauthorized', error_response),
            500: ('Server Error', error_response)
        }
    )
    @multi_auth_admin_required
    def get(self):
        """List all users (admin only)"""
        from app.routes.users import list_users
        return list_users()

@users_ns.route('/<int:user_id>')
class UserDetail(Resource):
    @api.doc('update_user',
        responses={
            200: ('Success', user_info),
            400: ('Bad Request', error_response),
            401: ('Unauthorized', error_response),
            404: ('Not Found', error_response),
            500: ('Server Error', error_response)
        }
    )
    @api.expect(register_model)
    @multi_auth_admin_required
    def put(self, user_id):
        """Update user details (admin only)"""
        from app.routes.users import update_user
        return update_user(user_id) 