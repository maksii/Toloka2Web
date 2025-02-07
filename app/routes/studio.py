from flask import Blueprint, jsonify, render_template, request, make_response
from flask_login import login_required

from app.services.services_db import DatabaseService


studio_bp = Blueprint('studio', __name__)


@studio_bp.route('/studios')
@login_required
def studios():
    return render_template('studios.html')

@studio_bp.route('/studios/<int:studio_id>')
@login_required
def studio_detail(studio_id):
    return render_template('studio_detail.html', studio_id=studio_id)

@studio_bp.route('/api/studio', methods=['GET'])
@login_required
def search_studio():
    try:
        query = request.args.get('query')
        if query:
            result = DatabaseService.search_studio_by_name(query)
        else:
            result = DatabaseService.list_all_studios()
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to search studios",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@studio_bp.route('/api/studio/<int:studio_id>', methods=['GET'])
@login_required
def get_studio_details(studio_id):
    try:
        result = DatabaseService.search_studio_by_id(studio_id)
        if not result:
            return make_response(jsonify({"error": "Studio not found"}), 404)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch studio details",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@studio_bp.route('/api/studio/<int:studio_id>/anime', methods=['GET'])
@login_required
def list_titles_by_studio(studio_id):
    try:
        result = DatabaseService.get_anime_by_studio_id(studio_id)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch studio anime list",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)