from flask import Blueprint, jsonify, render_template, request

from app.services_db import get_anime_by_studio_id, list_all_studios, search_studio_by_id, search_studio_by_name


studio_bp = Blueprint('studio', __name__)


@studio_bp.route('/studios')
def studios():
    return render_template('studios.html')

@studio_bp.route('/studios/<int:studio_id>')
def studio_detail(studio_id):
    return render_template('studio_detail.html', studio_id=studio_id)

@studio_bp.route('/api/studio', methods=['GET'])
def search_voice_studio():
    query = request.args.get('query')
    if query:
        return jsonify(search_studio_by_name(query))
    return jsonify(list_all_studios())

@studio_bp.route('/api/studio/<int:studio_id>', methods=['GET'])
def get_studio_details(studio_id):
    return jsonify(search_studio_by_id(studio_id))

@studio_bp.route('/api/studio/<int:studio_id>/anime', methods=['GET'])
def list_titles_by_studio(studio_id):
    return jsonify(get_anime_by_studio_id(studio_id))