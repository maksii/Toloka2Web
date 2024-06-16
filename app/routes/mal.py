from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.mal_service import search_anime, get_anime_detail

mal_bp = Blueprint('mal_bp', __name__)

@mal_bp.route('/api/mal/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    return jsonify(search_anime(query))

@mal_bp.route('/api/mal/detail/<int:anime_id>', methods=['GET'])
@login_required
def get_detail(anime_id):
    return jsonify(get_anime_detail(anime_id))