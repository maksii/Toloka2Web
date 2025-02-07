from flask import Blueprint, request, jsonify, make_response
from flask_login import login_required
from app.services.tmdb_service import TMDBService

tmdb_bp = Blueprint('tmdb_bp', __name__)

@tmdb_bp.route('/api/tmdb/search', methods=['GET'])
@login_required
def search():
    try:
        query = request.args.get('query')
        if not query:
            return make_response(jsonify({"error": "Query parameter is required"}), 400)
        result = TMDBService.search_media(query)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to search TMDB media",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@tmdb_bp.route('/api/tmdb/detail/<int:id>', methods=['GET'])
@login_required
def get_detail(id):
    try:
        media_type = request.args.get('type')
        if not media_type:
            return make_response(jsonify({"error": "Media type parameter is required"}), 400)
        result = TMDBService.get_media_detail(id, media_type)
        if not result:
            return make_response(jsonify({"error": "Media not found"}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch TMDB media details",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@tmdb_bp.route('/api/tmdb/trending', methods=['GET'])
@login_required
def get_trending():
    try:
        media_type = request.args.get('type')
        if not media_type:
            return make_response(jsonify({"error": "Media type parameter is required"}), 400)
        result = TMDBService.get_trending_by_type(media_type)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch trending media",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)