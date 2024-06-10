from flask import Blueprint, jsonify, render_template, request

from app.services import add_torrent_logic, get_torrent_logic, get_torrents_logic
from app.services_db import get_anime_by_studio_id, list_all_studios, search_studio_by_id, search_studio_by_name


toloka_bp = Blueprint('toloka', __name__)

@toloka_bp.route('/api/toloka', methods=['GET'])
def get_torrents():
    query = request.args.get('query')
    return jsonify(get_torrents_logic(query))

@toloka_bp.route('/api/toloka/<string:release_id>', methods=['GET'])
def get_torrent(release_id):
    return jsonify(get_torrent_logic(release_id))

@toloka_bp.route('/api/toloka/<string:release_id>', methods=['POST'])
def add_torrent(release_id):
    return jsonify(add_torrent_logic(release_id))