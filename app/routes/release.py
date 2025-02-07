from flask import Blueprint, jsonify, request, make_response
from flask_login import login_required
import jsonpickle

from app.services.route_service import RouteService
from app.services.services import TolokaService, TorrentService
from app.services.config_service import ConfigService

release_bp = Blueprint('release', __name__)

@release_bp.route('/api/releases', methods=['GET'])
@login_required
def get_titles():
    try:
        titles_data = TolokaService.get_titles_logic()
        torrents_data = TorrentService.get_releases_torrent_status()

        # Convert the list of torrents into a dictionary for easier access
        torrents_dict = {torrent['hash']: torrent for torrent in torrents_data.data if isinstance(torrent, dict)}

        # Extend each title with torrent info
        for title, data in titles_data.items():
            hash_value = data.get('hash')
            if hash_value in torrents_dict:
                # Only select relevant torrent info to add
                torrent_info = {
                    "state": torrents_dict[hash_value].get("state"),
                    "progress": torrents_dict[hash_value].get("progress"),
                    "name": torrents_dict[hash_value].get("name"),
                }
                data['torrent_info'] = torrent_info

        return make_response(jsonify(titles_data), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch titles",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@release_bp.route('/api/releases', methods=['POST'])
@login_required
def add_release():
    try:
        if not request.form:
            return make_response(jsonify({"error": "Request form data is required"}), 400)
            
        response = TolokaService.add_release_logic(request.form)
        ConfigService.sync_settings("release", "from")
        return make_response(jsonify(response), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to add release",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@release_bp.route('/api/releases/update', methods=['POST'])
@RouteService.login_or_api_key_required
def update_release():
    try:
        if request.form:
            response = TolokaService.update_release_logic(request.form)
        else:
            response = TolokaService.update_all_releases_logic()
            
        ConfigService.sync_settings("release", "from")
        return make_response(jsonify(response), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to update release",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@release_bp.route('/api/releases/torrents', methods=['GET'])
@RouteService.login_or_api_key_required
def torrent_info_all_releases():
    try:
        result = TorrentService.get_releases_torrent_status()
        return make_response(jsonpickle.encode(result, unpicklable=False), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch torrent info",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@release_bp.route('/api/releases/<string:hash>', methods=['GET'])
@RouteService.login_or_api_key_required
def recieve_request_from_client(hash):
    try:
        if not hash:
            return make_response(jsonify({"error": "Hash parameter is required"}), 400)
        return make_response(jsonify({"msg": f"{hash}"}), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to process client request",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@release_bp.route('/api/releases', methods=['PUT'])
@login_required
def edit_release():
    try:
        if not request.form:
            return make_response(jsonify({"error": "Request form data is required"}), 400)
            
        response = ConfigService.edit_release(request.form)
        return make_response(jsonify({"msg": response}), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to edit release",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@release_bp.route('/api/releases', methods=['DELETE'])
@login_required
def delete_release():
    try:
        if not request.form:
            return make_response(jsonify({"error": "Request form data is required"}), 400)
            
        response = ConfigService.delete_release(request.form)
        return make_response(jsonify({"msg": response}), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to delete release",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)