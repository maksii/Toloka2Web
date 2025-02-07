from flask import Blueprint, jsonify, render_template, request, make_response
from flask_login import login_required
from app.utils.auth_utils import multi_auth_required
from app.services.services_db import DatabaseService

anime_bp = Blueprint('anime', __name__)

@anime_bp.route('/anime')
@login_required
def anime():
    return render_template('anime.html')

@anime_bp.route('/anime/<int:anime_id>')
@login_required
def anime_detail(anime_id):
    return render_template('anime_detail.html', anime_id=anime_id)

@anime_bp.route('/api/anime', methods=['GET'])
@multi_auth_required
def list_anime():
    try:
        query = request.args.get('query')
        if query:
            result = DatabaseService.get_anime_by_name(query)
        else:
            result = DatabaseService.list_all_anime()
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch anime list",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@anime_bp.route('/api/anime/<int:anime_id>', methods=['GET'])
@multi_auth_required
def get_anime_byid(anime_id):
    try:
        result = DatabaseService.get_anime_by_id(anime_id)
        if not result:
            return make_response(jsonify({"error": "Anime not found"}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch anime details",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@anime_bp.route('/api/anime/<int:anime_id>/related', methods=['GET'])
@login_required
def get_anime_related(anime_id):
    try:
        result = DatabaseService.get_related_animes(anime_id)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch related anime",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@anime_bp.route('/api/anime/<int:anime_id>/studios', methods=['GET'])
@login_required
def get_anime_studios(anime_id):
    try:
        result = DatabaseService.get_studios_by_anime_id(anime_id)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch anime studios",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)