from flask import Blueprint, jsonify, request, make_response
from flask_login import login_required
from flask_principal import Permission, UserNeed, RoleNeed, identity_changed, Identity, AnonymousIdentity, identity_loaded

from app.services.config_service import ConfigService
from app.services.route_service import RouteService

setting_bp = Blueprint('setting', __name__)
admin_permission = Permission(RoleNeed('admin'))

@setting_bp.route('/api/settings', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def list_setting():
    try:
        result = ConfigService.read_all_settings_from_db()
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch settings",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@setting_bp.route('/api/settings', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def add():
    try:
        if not request.form:
            return make_response(jsonify({"error": "Request form data is required"}), 400)
            
        section = request.form.get('section')
        key = request.form.get('key')
        value = request.form.get('value')
        
        if not all([section, key, value]):
            return make_response(jsonify({"error": "Section, key, and value are required"}), 400)
            
        result = ConfigService.add_new_setting(section, key, value)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to add setting",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@setting_bp.route('/api/settings/<int:setting_id>', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def update(setting_id):
    try:
        if not request.form:
            return make_response(jsonify({"error": "Request form data is required"}), 400)
            
        section = request.form.get('section')
        key = request.form.get('key')
        value = request.form.get('value')
        
        if not all([section, key, value]):
            return make_response(jsonify({"error": "Section, key, and value are required"}), 400)
            
        result = ConfigService.update_setting(setting_id, section, key, value)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to update setting",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@setting_bp.route('/api/settings/sync', methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def sync():
    try:
        if not request.form:
            return make_response(jsonify({"error": "Request form data is required"}), 400)
            
        direction = request.form.get('direction')
        type = request.form.get('type')
        
        if not all([direction, type]):
            return make_response(jsonify({"error": "Direction and type are required"}), 400)
            
        result = ConfigService.sync_settings(type, direction)
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to sync settings",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@setting_bp.route('/api/settings/versions', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def versions():
    try:
        packages = RouteService.get_installed_packages()
        return make_response(jsonify(packages), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to fetch package versions",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)

@setting_bp.route('/api/settings/files', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def check_config_files():
    try:
        result = RouteService.list_files("app/data")
        return make_response(jsonify(result), 200)
    except Exception as e:
        error_message = {
            "error": "Failed to list configuration files",
            "details": str(e)
        }
        return make_response(jsonify(error_message), 500)