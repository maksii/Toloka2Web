from flask import Blueprint, jsonify, request, make_response
from app.utils.auth_utils import multi_auth_required
import jsonpickle

from app.services.services import StreamingService

stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/api/stream', methods=['GET'])
@multi_auth_required
def search_titles_from_streaming():
    try:
        query = request.args.get('query')
        if not query:
            return make_response(jsonify({"error": "Query parameter is required"}), 400)
        result = StreamingService.search_titles_from_streaming_site(query)
        return make_response(jsonpickle.encode(result, unpicklable=False), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to search streaming titles",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@stream_bp.route('/api/stream', methods=['POST'])
@multi_auth_required
def add_title_from_streaming():
    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Request body is required"}), 400)
        result = StreamingService.add_title_from_streaming_site(data)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to add streaming title",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@stream_bp.route('/api/stream/details', methods=['POST'])
@multi_auth_required
def get_title_details():
    try:
        data = request.get_json()
        if not data or 'provider' not in data or 'link' not in data:
            return make_response(jsonify({"error": "Provider and link are required"}), 400)
        result = StreamingService.get_streaming_site_release_details(data['provider'], data['link'])
        return make_response(jsonpickle.encode(result, unpicklable=False), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch streaming title details",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)