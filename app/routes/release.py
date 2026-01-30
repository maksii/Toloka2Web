"""Release routes for managing torrent releases."""
from flask import Blueprint, jsonify, request, make_response
import jsonpickle

from app.utils.auth_utils import multi_auth_required
from app.utils.errors import handle_errors, ValidationError
from app.services.services import TolokaService, TorrentService
from app.services.config_service import ConfigService

release_bp = Blueprint('release', __name__)


@release_bp.route('/releases', methods=['GET'])
@multi_auth_required
@handle_errors
def get_titles():
    """Get all releases with their torrent status."""
    titles_data = TolokaService.get_titles_with_torrent_status()
    return make_response(jsonify(titles_data), 200)


@release_bp.route('/releases', methods=['POST'])
@multi_auth_required
@handle_errors
def add_release():
    """Add a new release."""
    data = request.get_json() if request.is_json else request.form
    if not data:
        raise ValidationError("Request data is required")
        
    response = TolokaService.add_release_logic(data)
    ConfigService.sync_settings("release", "from")
    return make_response(jsonify(response), 200)


@release_bp.route('/releases/update', methods=['POST'])
@multi_auth_required
@handle_errors
def update_release():
    """Update release(s) - if no data provided, updates all releases."""
    data = request.get_json() if request.is_json else request.form
    if data:
        response = TolokaService.update_release_logic(data)
    else:
        response = TolokaService.update_all_releases_logic()
        
    ConfigService.sync_settings("release", "from")
    return make_response(jsonify(response), 200)


@release_bp.route('/releases/torrents', methods=['GET'])
@multi_auth_required
@handle_errors
def torrent_info_all_releases():
    """Get torrent info for all releases."""
    result = TorrentService.get_releases_torrent_status()
    return make_response(jsonpickle.encode(result, unpicklable=False), 200)


@release_bp.route('/releases/<string:hash>', methods=['GET'])
@multi_auth_required
@handle_errors
def recieve_request_from_client(hash):
    """Get release by hash."""
    if not hash:
        raise ValidationError("Hash parameter is required")
    return make_response(jsonify({"msg": f"{hash}"}), 200)


@release_bp.route('/releases', methods=['PUT'])
@multi_auth_required
@handle_errors
def edit_release():
    """Edit an existing release."""
    data = request.get_json() if request.is_json else request.form
    if not data:
        raise ValidationError("Request data is required")
        
    response = ConfigService.edit_release(data)
    return make_response(jsonify({"msg": response}), 200)


@release_bp.route('/releases', methods=['DELETE'])
@multi_auth_required
@handle_errors
def delete_release():
    """Delete a release."""
    data = request.get_json() if request.is_json else request.form
    if not data:
        raise ValidationError("Request data is required")
        
    response = ConfigService.delete_release(data)
    return make_response(jsonify({"msg": response}), 200)
