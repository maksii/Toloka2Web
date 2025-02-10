# Flask and extensions
from flask import Blueprint, jsonify, request, make_response

# Local imports
from app.utils.auth_utils import multi_auth_required
from app.services.services import TolokaService

toloka_bp = Blueprint('toloka', __name__)

@toloka_bp.route('/api/toloka', methods=['GET'])
@multi_auth_required
def get_torrents():
    try:
        query = request.args.get('query')
        result = TolokaService.get_torrents_logic(query)
        
        # Check if the response is a "No results found" message
        if isinstance(result, str) and result.startswith("No results found"):
            return make_response(jsonify({"error": result}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch torrents",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@toloka_bp.route('/api/toloka/<string:release_id>', methods=['GET'])
@multi_auth_required
def get_torrent(release_id):
    try:
        result = TolokaService.get_torrent_logic(release_id)
        if not result:
            return make_response(jsonify({"error": "Torrent not found"}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch torrent details",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@toloka_bp.route('/api/toloka', methods=['POST'])
@multi_auth_required
def add_torrent():
    try:
        if not request.form and not request.get_json():
            return make_response(jsonify({"error": "Request data is required"}), 400)
        result = TolokaService.add_torrent_logic(request)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to add torrent",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)