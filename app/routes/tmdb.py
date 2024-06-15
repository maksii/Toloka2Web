from flask import Blueprint, request, jsonify
from app.services.tmdb_service import search_movie, get_movie_detail

tmdb_bp = Blueprint('tmdb_bp', __name__)

@tmdb_bp.route('/api/tmdb/search', methods=['GET'])
def search():
    query = request.args.get('query')
    return jsonify(search_movie(query))

@tmdb_bp.route('/api/tmdb/detail/<int:movie_id>', methods=['GET'])
def get_detail(movie_id):
    return jsonify(get_movie_detail(movie_id))