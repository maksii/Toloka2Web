from flask import Blueprint, jsonify, request
from flask_login import login_required

from app.services import add_release_logic, get_titles_logic, update_all_releases_logic, update_release_logic

release_bp = Blueprint('release', __name__)

@release_bp.route('/api/releases', methods=['GET'])
@login_required
def get_titles():
    return jsonify(get_titles_logic())

@release_bp.route('/api/releases', methods=['POST'])
@login_required
def add_release():
    return jsonify(add_release_logic(request.form))

@release_bp.route('/api/releases/update', methods=['POST'])
@login_required
def update_release():
    return jsonify(update_release_logic(request.form))

@release_bp.route('/api/releases/', methods=['POST'])
@login_required
def update_all_releases():
    return jsonify(update_all_releases_logic())