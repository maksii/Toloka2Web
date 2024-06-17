from flask import Blueprint, jsonify, make_response, request
from flask_login import login_required

from app.services.services import add_torrent_logic, get_torrent_logic, get_torrents_logic


toloka_bp = Blueprint('toloka', __name__)

@toloka_bp.route('/api/toloka', methods=['GET'])
@login_required
def get_torrents():
    try:
        query = request.args.get('query')
        response = get_torrents_logic(query)
        
        # Check if the response is a "No results found" message
        if isinstance(response, str) and response.startswith("No results found"):
            return jsonify({"error": response})
        else:
            return jsonify(response)
    except Exception as e:
        # Return a custom JSON error message with a 500 Internal Server Error status
        error_message = {
            "error": "app.ini or other configuration not valid, please check your configs",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@toloka_bp.route('/api/toloka/<string:release_id>', methods=['GET'])
@login_required
def get_torrent(release_id):
    return jsonify(get_torrent_logic(release_id))

@toloka_bp.route('/api/toloka/', methods=['POST'])
@login_required
def add_torrent():
    return jsonify(add_torrent_logic(request))