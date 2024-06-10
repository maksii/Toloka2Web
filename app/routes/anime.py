from flask import Blueprint, jsonify, render_template, request

from app.services_db import get_anime_by_id, get_anime_by_name, get_related_animes, get_studios_by_anime_id, list_all_anime

anime_bp = Blueprint('anime', __name__)

@anime_bp.route('/anime')
def anime():
    return render_template('anime.html')

@anime_bp.route('/anime/<int:anime_id>')
def anime_detail(anime_id):
    return render_template('anime_detail.html', anime_id=anime_id)

@anime_bp.route('/api/anime', methods=['GET'])
def list_anime():
    query = request.args.get('query')
    if query:
        return jsonify(get_anime_by_name(query))
    return jsonify(list_all_anime())

@anime_bp.route('/api/anime/<int:anime_id>', methods=['GET'])
def get_anime_byid(anime_id):
    return jsonify(get_anime_by_id(anime_id))

@anime_bp.route('/api/anime/<int:anime_id>/related', methods=['GET'])
def get_anime_by_id_related(anime_id):
    return jsonify(get_related_animes(anime_id))

@anime_bp.route('/api/anime/<int:anime_id>/studios', methods=['GET'])
def get_anime_by_id_studios(anime_id):
    return jsonify(get_studios_by_anime_id(anime_id))