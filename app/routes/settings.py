"""Settings routes for application configuration."""

from flask import Blueprint, jsonify, request, make_response
from flask_login import login_required
from flask_principal import Permission, RoleNeed

from app.utils.auth_utils import multi_auth_admin_required
from app.utils.errors import handle_errors, ValidationError
from app.services.config_service import ConfigService
from app.services.route_service import RouteService

setting_bp = Blueprint("setting", __name__)
admin_permission = Permission(RoleNeed("admin"))


@setting_bp.route("/settings", methods=["GET"])
@multi_auth_admin_required
@handle_errors
def list_setting():
    """List all application settings."""
    result = ConfigService.read_all_settings_from_db()
    return make_response(jsonify(result), 200)


@setting_bp.route("/settings", methods=["POST"])
@multi_auth_admin_required
@handle_errors
def add():
    """Add a new application setting."""
    data = request.get_json() if request.is_json else request.form
    if not data:
        raise ValidationError("Request data is required")

    section = data.get("section")
    key = data.get("key")
    value = data.get("value")

    if not all([section, key, value]):
        raise ValidationError("Section, key, and value are required")

    result = ConfigService.add_new_setting(section, key, value)
    return make_response(jsonify(result), 200)


@setting_bp.route("/settings/<int:setting_id>", methods=["POST"])
@login_required
@admin_permission.require(http_exception=403)
@handle_errors
def update(setting_id):
    """Update an existing setting."""
    if not request.form:
        raise ValidationError("Request form data is required")

    section = request.form.get("section")
    key = request.form.get("key")
    value = request.form.get("value")

    if not all([section, key, value]):
        raise ValidationError("Section, key, and value are required")

    result = ConfigService.update_setting(setting_id, section, key, value)
    return make_response(jsonify(result), 200)


@setting_bp.route("/settings/sync", methods=["POST"])
@login_required
@admin_permission.require(http_exception=403)
@handle_errors
def sync():
    """Sync settings between database and INI files."""
    if not request.form:
        raise ValidationError("Request form data is required")

    direction = request.form.get("direction")
    type = request.form.get("type")

    if not all([direction, type]):
        raise ValidationError("Direction and type are required")

    result = ConfigService.sync_settings(type, direction)
    return make_response(jsonify(result), 200)


@setting_bp.route("/settings/versions", methods=["GET"])
@login_required
@admin_permission.require(http_exception=403)
@handle_errors
def versions():
    """Get installed package versions."""
    packages = RouteService.get_installed_packages()
    return make_response(jsonify(packages), 200)


@setting_bp.route("/settings/files", methods=["GET"])
@login_required
@admin_permission.require(http_exception=403)
@handle_errors
def check_config_files():
    """List configuration files."""
    result = RouteService.list_files("app/data")
    return make_response(jsonify(result), 200)
