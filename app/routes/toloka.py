from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.services import add_torrent_logic, get_torrent_logic, get_torrents_logic


toloka_bp = Blueprint('toloka', __name__)

@toloka_bp.route('/api/toloka', methods=['GET'])
@login_required
def get_torrents():
    query = request.args.get('query')
    return jsonify(get_torrents_logic(query))

@toloka_bp.route('/api/toloka/<string:release_id>', methods=['GET'])
@login_required
def get_torrent(release_id):
    return jsonify(get_torrent_logic(release_id))

@toloka_bp.route('/api/toloka/<string:release_id>', methods=['POST'])
@login_required
def add_torrent(release_id):
    return jsonify(add_torrent_logic(release_id))