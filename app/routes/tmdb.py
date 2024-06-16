from flask import Blueprint, request, jsonify
from flask_login import login_required
from app.services.tmdb_service import get_media_detail, search_media

tmdb_bp = Blueprint('tmdb_bp', __name__)

@tmdb_bp.route('/api/tmdb/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    return jsonify(search_media(query))

@tmdb_bp.route('/api/tmdb/detail/<int:id>', methods=['GET'])
@login_required
def get_detail(id):
    query = request.args.get('type')
    return jsonify(get_media_detail(id, query))