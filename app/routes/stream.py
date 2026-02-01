# Standard library imports
import time

# Third-party imports
import jsonpickle
from flask import Blueprint, jsonify, request, make_response

# Local imports
from app.utils.auth_utils import multi_auth_required
from app.services.services import StreamingService

stream_bp = Blueprint("stream", __name__)

# In-memory cache for stream responses: key -> (encoded_response, expiry_time)
_STREAM_CACHE = {}
_STREAM_CACHE_TTL = 300  # seconds


def _cache_get(key):
    """Return cached value if present and not expired."""
    entry = _STREAM_CACHE.get(key)
    if not entry:
        return None
    body, expiry = entry
    if time.monotonic() > expiry:
        del _STREAM_CACHE[key]
        return None
    return body


def _cache_set(key, body):
    """Store response in cache with TTL."""
    _STREAM_CACHE[key] = (body, time.monotonic() + _STREAM_CACHE_TTL)


@stream_bp.route("/stream", methods=["GET"])
@multi_auth_required
def search_titles_from_streaming():
    try:
        query = request.args.get("query")
        if not query:
            return make_response(jsonify({"error": "Query parameter is required"}), 400)
        cache_key = ("search", query.strip())
        cached = _cache_get(cache_key)
        if cached is not None:
            return make_response(cached, 200)
        result = StreamingService.search_titles_from_streaming_site(query)
        encoded = jsonpickle.encode(result, unpicklable=False)
        _cache_set(cache_key, encoded)
        return make_response(encoded, 200)
    except Exception as e:
        error_message = {
            "error": "Failed to search streaming titles",
            "details": str(e),
        }
        return make_response(jsonify(error_message), 500)


@stream_bp.route("/stream", methods=["POST"])
@multi_auth_required
def add_title_from_streaming():
    try:
        data = request.get_json()
        if not data:
            return make_response(jsonify({"error": "Request body is required"}), 400)
        result = StreamingService.add_title_from_streaming_site(data)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {"error": "Failed to add streaming title", "details": str(e)}
        return make_response(jsonify(error_message), 500)


@stream_bp.route("/stream/details", methods=["POST"])
@multi_auth_required
def get_title_details():
    try:
        data = request.get_json()
        if not data or "provider" not in data or "link" not in data:
            return make_response(
                jsonify({"error": "Provider and link are required"}), 400
            )
        provider = data["provider"]
        link = data.get("link") or data.get("url", "")
        cache_key = ("details", provider, link)
        cached = _cache_get(cache_key)
        if cached is not None:
            return make_response(cached, 200)
        result = StreamingService.get_streaming_site_release_details(
            provider, link
        )
        encoded = jsonpickle.encode(result, unpicklable=False)
        _cache_set(cache_key, encoded)
        return make_response(encoded, 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch streaming title details",
            "details": str(e),
        }
        return make_response(jsonify(error_message), 500)
