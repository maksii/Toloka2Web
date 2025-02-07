# app/__main__.py

import os

import requests

from app.services.services_db import DatabaseService
from .app import create_app


def download_file(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb', encoding='utf-8') as f:
            f.write(response.content)
        print(f"File downloaded and saved as {path}.")
    except requests.RequestException as e:
        print(f"Failed to download the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def initialize_app():
    local_db_path = "data/anime_data.db"
    if not os.path.exists(local_db_path):
        print("Database not found. Downloading the database...")
        DatabaseService.update_database()
    else:
        print("Database already exists.")

    # Check and download app.ini if not exists
    app_ini_path = "data/app.ini"
    if not os.path.exists(app_ini_path):
        print("app.ini not found. Downloading the app.ini...")
        download_file("https://raw.githubusercontent.com/CakesTwix/Toloka2MediaServer/main/data/app-example.ini", app_ini_path)
    else:
        print("app.ini already exists.")

    # Check and create titles.ini if not exists
    titles_ini_path = "data/titles.ini"
    if not os.path.exists(titles_ini_path):
        print("titles.ini not found. Creating an empty titles.ini...")
        open(titles_ini_path, 'a', encoding='utf-8').close()  # This will create an empty file
    else:
        print("titles.ini already exists.")

initialize_app()
DatabaseService.initialize_database()
app = create_app()

if __name__ == '__main__':
    # Set the default port to 5000 if not specified
    port = int(os.getenv('PORT', 5000))
    # Set the default host to '0.0.0.0' to run on all network interfaces
    host = os.getenv('HOST', '0.0.0.0')

    # Run the Flask application with the specified host and port
    app.run(host=host, port=port)