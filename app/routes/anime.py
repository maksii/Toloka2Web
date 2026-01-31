"""Anime routes for HTML pages and API endpoints."""

from flask import Blueprint, jsonify, render_template, request, make_response
from flask_login import login_required

from app.utils.auth_utils import multi_auth_required
from app.utils.errors import handle_errors, NotFoundError
from app.services.services_db import DatabaseService

# Create two separate blueprints: one for HTML routes and one for API routes
anime_bp = Blueprint("anime", __name__)  # For HTML page routes
anime_api_bp = Blueprint("anime_api", __name__)  # For API routes


# HTML routes
@anime_bp.route("/anime")
@login_required
def anime():
    """Render the anime list page."""
    return render_template("anime.html")


@anime_bp.route("/anime/<int:anime_id>")
@login_required
def anime_detail(anime_id):
    """Render the anime detail page."""
    return render_template("anime_detail.html", anime_id=anime_id)


# API routes
@anime_api_bp.route("/anime", methods=["GET"])
@multi_auth_required
@handle_errors
def list_anime():
    """List all anime or search by name."""
    query = request.args.get("query")
    if query:
        result = DatabaseService.get_anime_by_name(query)
    else:
        result = DatabaseService.list_all_anime()
    return make_response(jsonify(result), 200)


@anime_api_bp.route("/anime/<int:anime_id>", methods=["GET"])
@multi_auth_required
@handle_errors
def get_anime_byid(anime_id):
    """Get anime details by ID."""
    result = DatabaseService.get_anime_by_id(anime_id)
    if not result:
        raise NotFoundError("Anime not found")
    return make_response(jsonify(result), 200)


@anime_api_bp.route("/anime/<int:anime_id>/related", methods=["GET"])
@login_required
@handle_errors
def get_anime_related(anime_id):
    """Get related anime for a given anime ID."""
    result = DatabaseService.get_related_animes(anime_id)
    return make_response(jsonify(result), 200)


@anime_api_bp.route("/anime/<int:anime_id>/studios", methods=["GET"])
@login_required
@handle_errors
def get_anime_studios(anime_id):
    """Get studios for a given anime ID."""
    result = DatabaseService.get_studios_by_anime_id(anime_id)
    return make_response(jsonify(result), 200)
