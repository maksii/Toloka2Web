# routes.py

from flask import jsonify, request, render_template, Response

from app.services_db import get_anime_by_id, get_anime_by_name, get_anime_by_studio_id, get_related_animes, get_studios_by_anime_id, list_all_anime, list_all_studios, search_studio_by_id, search_studio_by_name
from .services import (
    initiate_config, get_titles_logic, get_torrent_logic, add_torrent_logic,
    add_release_logic, update_release_logic, update_all_releases_logic,
    proxy_image_logic, get_torrents_logic, search_voice_studio, list_voice_studios,
    list_titles_by_studio, search_titles_from_streaming_site, add_title_from_streaming_site
)

def configure_routes(app):
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/studios')
    def studios():
        return render_template('studios.html')
    
    @app.route('/studios/<int:studio_id>')
    def studio_detail(studio_id):
        # You might fetch studio details from a database based on studio_id
        return render_template('studio_detail.html', studio_id=studio_id)

    @app.route('/anime')
    def anime():
        return render_template('anime.html')
    
    @app.route('/anime/<int:anime_id>')
    def anime_detail(anime_id):
        # You might fetch anime details from a database based on anime_id
        return render_template('anime_detail.html', anime_id=anime_id)
    
    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    @app.route('/get_titles', methods=['GET'])
    def get_titles():
        return jsonify(get_titles_logic())

    @app.route('/get_torrents', methods=['GET'])
    def get_torrents():
        query = request.args.get('query')
        return jsonify(get_torrents_logic(query))
    
    @app.route('/get_torrent', methods=['GET'])
    def get_torrent():
        query = request.args.get('id')
        return jsonify(get_torrent_logic(query))

    @app.route('/add_torrent', methods=['GET'])
    def add_torrent():
        id = request.args.get('id')
        return jsonify(add_torrent_logic(id))

    @app.route('/add_release', methods=['POST'])
    def add_release():
        return jsonify(add_release_logic(request.form))

    @app.route('/update_release', methods=['POST'])
    def update_release():
        return jsonify(update_release_logic(request.form))

    @app.route('/update_all_releases', methods=['POST'])
    def update_all_releases():
        return jsonify(update_all_releases_logic())

    @app.route('/image/')
    def proxy_image():
        url = request.args.get('url')
        return proxy_image_logic(url)

    # Placeholder routes for new endpoints
    @app.route('/search_voice_studio', methods=['GET'])
    def search_voice_studio():
        query = request.args.get('query')
        return jsonify(search_studio_by_name(query))

    @app.route('/list_voice_studios', methods=['GET'])
    def list_voice_studios():
        return jsonify(list_all_studios())

    @app.route('/list_titles_by_studio/<int:studio_id>', methods=['GET'])
    def list_titles_by_studio(studio_id):
        return jsonify(get_anime_by_studio_id(studio_id))
    
    @app.route('/get_studio_details/<int:studio_id>', methods=['GET'])
    def get_studio_details(studio_id):
        return jsonify(search_studio_by_id(studio_id))
    
    @app.route('/list_anime', methods=['GET'])
    def list_anime():
        return jsonify(list_all_anime())

    @app.route('/search_anime_by_name', methods=['GET'])
    def search_anime_by_name():
        query = request.args.get('query')
        return jsonify(get_anime_by_name(query))

    @app.route('/get_anime_by_id/<int:anime_id>', methods=['GET'])
    def get_anime_byid(anime_id):
        return jsonify(get_anime_by_id(anime_id))

    @app.route('/get_anime_by_id/<int:anime_id>/related', methods=['GET'])
    def get_anime_by_id_related(anime_id):
        return jsonify(get_related_animes(anime_id))

    @app.route('/get_anime_by_id/<int:anime_id>/studios', methods=['GET'])
    def get_anime_by_id_studios(anime_id):
        return jsonify(get_studios_by_anime_id(anime_id))

    @app.route('/search_titles_from_streaming_site', methods=['GET'])
    def search_titles_from_streaming_site():
        query = request.args.get('query')
        return jsonify(search_titles_from_streaming_site(query))

    @app.route('/add_title_from_streaming_site', methods=['POST'])
    def add_title_from_streaming_site():
        data = request.get_json()
        return jsonify(add_title_from_streaming_site(data))