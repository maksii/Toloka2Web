# services.py

from flask import Response
import requests
from toloka2MediaServer.config_parser import load_configurations, get_toloka_client
from toloka2MediaServer.clients.dynamic import dynamic_client_init
from toloka2MediaServer.models.config import Config
from toloka2MediaServer.logger_setup import setup_logging
from toloka2MediaServer.main_logic import (
    add_release_by_url, update_release_by_name, update_releases,
    search_torrents, get_torrent as get_torrent_external,
    add_torrent as add_torrent_external
)

from app.models.request_data import RequestData

def initiate_config():
    app_config_path='data/app.ini'
    title_config_path='data/titles.ini'
    logger_path = 'data/app_web.log'

    app_config, titles_config, application_config = load_configurations(app_config_path,title_config_path)
    toloka=get_toloka_client(application_config)
    logger=setup_logging(logger_path)

    config = Config(
        logger=logger,
        toloka=toloka,
        app_config=app_config,
        titles_config=titles_config,
        application_config=application_config
    )

    client = dynamic_client_init(config)
    config.client = client
    
    return config

def get_titles_logic():
    config = initiate_config()
    sections = {}
    for section in config.titles_config.sections():
        options = {}
        for option in config.titles_config.options(section):
            options[option] = config.titles_config.get(section, option)
        sections[section] = options
    return sections

def get_torrents_logic(query):
    if query:
        config = initiate_config()
        config.args = query
        torrent = search_torrents(config)
        return torrent
    else:
        return {}
    
def get_torrent_logic(id):
    if id:
        config = initiate_config()
        config.args = id
        torrent = get_torrent_external(config)
        return torrent
    else:
        return {}

def add_torrent_logic(id):
    if id:
        config = initiate_config()
        config.args = id
        output = add_torrent_external(config)
        return output
    else:
        return {}
    
def add_release_logic(request):
    # Process the URL to add release
    try:
        config = initiate_config()
        requestData = RequestData(
            url = request['url'],
            season = request['season'],
            index = int(request['index']),
            correction = int(request['correction']),
            title = request['title'],
        )


        #--add --url https://toloka.to/t675888 --season 02 --index 2 --correction 0 --title "Tsukimichi -Moonlit Fantasy-"
        config.args = requestData
        operation_result = add_release_by_url(config)
        output = serialize_operation_result(operation_result)
        return output
    except Exception as e:
        message = f'Error: {str(e)}'
        return f'{"error": {message}}'
    
def update_release_logic(request):
    # Process the name to update release
    try:
        config = initiate_config()
        requestData = RequestData(
            codename = request['codename']
        )
        config.args = requestData
        operation_result = update_release_by_name(config)
        output = serialize_operation_result(operation_result)
        
        return output
    except Exception as e:
        message = f'Error: {str(e)}'
        return f'{"error": {message}}'

def update_all_releases_logic(request):
    # Process to update all releases
    try:
        config = initiate_config()
        requestData = RequestData()
        config.args = requestData
        operation_result = update_releases(config)
        output = serialize_operation_result(operation_result)
        
        return output
    except Exception as e:
        message = f'Error: {str(e)}'
        return f'{"error": {message}}'

def serialize_operation_result(operation_result):
    return {
        "operation_type": operation_result.operation_type.name if operation_result.operation_type else None,
        "torrent_references": [str(torrent) for torrent in operation_result.torrent_references],
        "titles_references": [str(titles) for titles in operation_result.titles_references],    
        "status_message": operation_result.status_message,
        "response_code": operation_result.response_code.name if operation_result.response_code else None,
        "operation_logs": operation_result.operation_logs,
        "start_time": operation_result.start_time.isoformat() if operation_result.start_time else None,
        "end_time": operation_result.end_time.isoformat() if operation_result.end_time else None
    }
# Additional functions for other endpoints would be added here...

def proxy_image_logic(url):
    if not url:
        return "No URL provided", 400

    # Normalize the URL
    if url.startswith('//'):
        url = 'https:' + url  # Assume https if protocol is missing
    elif not url.startswith(('http://', 'https://')):
        url = 'https://' + url  # Assume https if only hostname is provided
        
    # Send a GET request to the image URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    }
    response = requests.get(url, headers=headers, stream=True)

    # Check if the request was successful
    if response.status_code != 200:
        return "Failed to fetch image", response.status_code

    # Stream the response content directly to the client
    return Response(response.iter_content(chunk_size=1024), content_type=response.headers['Content-Type'])
    pass

# Placeholder functions for new endpoints
def search_voice_studio(query):
    # Logic for searching voice studios
    pass

def list_voice_studios():
    # Logic for listing voice studios
    pass

def list_titles_by_studio(studio_id):
    # Logic for listing titles by a specific studio
    pass

def search_titles_from_streaming_site(query):
    # Logic for searching titles from a streaming site
    pass

def add_title_from_streaming_site(data):
    # Logic for adding a title from a streaming site
    pass