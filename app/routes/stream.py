from flask import Blueprint, jsonify, request
import jsonpickle

from app.services.services import add_title_from_streaming_site, search_titles_from_streaming_site


stream_bp = Blueprint('stream', __name__)

@stream_bp.route('/api/stream', methods=['GET'])
def search_titles_from_streaming():
    query = request.args.get('query')
    return jsonpickle.encode(search_titles_from_streaming_site(query))

@stream_bp.route('/api/stream', methods=['POST'])
def add_title_from_streaming():
    data = request.get_json()
    return jsonify(add_title_from_streaming_site(data))