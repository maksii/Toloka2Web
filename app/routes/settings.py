from flask import Blueprint, jsonify

from app.services.config_service import read_all_settings_from_db


setting_bp = Blueprint('setting', __name__)

@setting_bp.route('/api/settings', methods=['GET'])
def list_setting():
    return jsonify(read_all_settings_from_db())