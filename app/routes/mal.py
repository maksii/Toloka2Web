from flask import Blueprint, request, jsonify, make_response
from app.utils.auth_utils import multi_auth_required
from app.services.mal_service import MALService

mal_bp = Blueprint('mal_bp', __name__)

@mal_bp.route('/api/mal/search', methods=['GET'])
@multi_auth_required
def search():
    try:
        query = request.args.get('query')
        if not query:
            return make_response(jsonify({"error": "Query parameter is required"}), 400)
        result = MALService.search_anime(query)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to search MAL anime",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@mal_bp.route('/api/mal/detail/<int:anime_id>', methods=['GET'])
@multi_auth_required
def get_detail(anime_id):
    try:
        result = MALService.get_anime_detail(anime_id)
        if not result:
            return make_response(jsonify({"error": "Anime not found"}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch MAL anime details",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)