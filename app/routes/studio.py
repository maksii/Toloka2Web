"""Studio routes for HTML pages and API endpoints."""

from flask import Blueprint, jsonify, render_template, request, make_response
from flask_login import login_required

from app.utils.auth_utils import multi_auth_required
from app.utils.errors import handle_errors, NotFoundError
from app.services.services_db import DatabaseService

# Create two separate blueprints: one for HTML routes and one for API routes
studio_bp = Blueprint("studio", __name__)  # For HTML page routes
studio_api_bp = Blueprint("studio_api", __name__)  # For API routes


# HTML routes
@studio_bp.route("/studios")
@login_required
def studios():
    """Render the studios list page."""
    return render_template("studios.html")


@studio_bp.route("/studios/<int:studio_id>")
@login_required
def studio_detail(studio_id):
    """Render the studio detail page."""
    return render_template("studio_detail.html", studio_id=studio_id)


# API routes
@studio_api_bp.route("/studio", methods=["GET"])
@multi_auth_required
@handle_errors
def search_studio():
    """Search studios by name or list all."""
    query = request.args.get("query")
    if query:
        result = DatabaseService.search_studio_by_name(query)
    else:
        result = DatabaseService.list_all_studios()
    return make_response(jsonify(result), 200)


@studio_api_bp.route("/studio/<int:studio_id>", methods=["GET"])
@multi_auth_required
@handle_errors
def get_studio_details(studio_id):
    """Get studio details by ID."""
    result = DatabaseService.search_studio_by_id(studio_id)
    if not result:
        raise NotFoundError("Studio not found")
    return make_response(jsonify(result), 200)


@studio_api_bp.route("/studio/<int:studio_id>/anime", methods=["GET"])
@multi_auth_required
@handle_errors
def list_titles_by_studio(studio_id):
    """List anime from a specific studio."""
    result = DatabaseService.get_anime_by_studio_id(studio_id)
    return make_response(jsonify(result), 200)
