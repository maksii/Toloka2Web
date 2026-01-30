"""Toloka routes for torrent search and management."""
from flask import Blueprint, jsonify, request, make_response

from app.utils.auth_utils import multi_auth_required
from app.utils.errors import handle_errors, ValidationError, NotFoundError
from app.services.services import TolokaService

toloka_bp = Blueprint('toloka', __name__)


@toloka_bp.route('/toloka', methods=['GET'])
@multi_auth_required
@handle_errors
def get_torrents():
    """Search for torrents on Toloka."""
    query = request.args.get('query')
    result = TolokaService.get_torrents_logic(query)
    
    # Check if the response is a "No results found" message
    if isinstance(result, str) and result.startswith("No results found"):
        raise NotFoundError(result)
    return make_response(jsonify(result), 200)


@toloka_bp.route('/toloka/<string:release_id>', methods=['GET'])
@multi_auth_required
@handle_errors
def get_torrent(release_id):
    """Get torrent details by release ID."""
    result = TolokaService.get_torrent_logic(release_id)
    if not result:
        raise NotFoundError('Torrent not found')
    return make_response(jsonify(result), 200)


@toloka_bp.route('/toloka', methods=['POST'])
@multi_auth_required
@handle_errors
def add_torrent():
    """Add a torrent from Toloka."""
    if not request.form and not request.get_json():
        raise ValidationError("Request data is required")
    result = TolokaService.add_torrent_logic(request)
    return make_response(jsonify(result), 200)
