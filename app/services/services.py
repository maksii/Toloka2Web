# services.py

from typing import Dict, Any, List
from flask import Response, json
import requests

from toloka2MediaServer.config_parser import load_configurations, get_toloka_client
from toloka2MediaServer.clients.dynamic import dynamic_client_init
from toloka2MediaServer.models.config import Config
from toloka2MediaServer.logger_setup import setup_logging
from toloka2MediaServer.main_logic import (
    add_release_by_url,
    update_release_by_name,
    update_releases,
    search_torrents,
    get_torrent as get_torrent_external,
    add_torrent as add_torrent_external,
)
from stream2mediaserver.main_logic import MainLogic

from app.models.request_data import RequestData
from app.services.base_service import BaseService
from app.services.mal_service import MALService
from app.services.tmdb_service import TMDBService
from app.services.services_db import DatabaseService


class TolokaService(BaseService):
    """Service for handling Toloka-related operations."""

    CONFIG_PATHS = {
        "app": "data/app.ini",
        "titles": "data/titles.ini",
        "logger": "data/app_web.log",
    }

    @classmethod
    def initiate_config(cls) -> Config:
        """Initialize full configuration with Toloka client."""
        app_config, titles_config, application_config = load_configurations(
            cls.CONFIG_PATHS["app"], cls.CONFIG_PATHS["titles"]
        )
        toloka = get_toloka_client(application_config)
        logger = setup_logging(cls.CONFIG_PATHS["logger"])

        config = Config(
            logger=logger,
            toloka=toloka,
            app_config=app_config,
            titles_config=titles_config,
            application_config=application_config,
        )

        client = dynamic_client_init(config)
        config.client = client

        return config

    @classmethod
    def initiate_min_config(cls) -> Config:
        """Initialize minimal configuration without Toloka client."""
        app_config, titles_config, application_config = load_configurations(
            cls.CONFIG_PATHS["app"], cls.CONFIG_PATHS["titles"]
        )
        logger = setup_logging(cls.CONFIG_PATHS["logger"])

        return Config(
            logger=logger,
            app_config=app_config,
            titles_config=titles_config,
            application_config=application_config,
        )

    @classmethod
    def get_titles_logic(cls) -> Dict:
        """Get all titles configuration."""
        config = cls.initiate_min_config()
        sections = {}
        for section in config.titles_config.sections():
            options = {}
            for option in config.titles_config.options(section):
                options[option] = config.titles_config.get(section, option)
            sections[section] = options
        return sections

    @classmethod
    def get_titles_with_torrent_status(cls) -> Dict:
        """Get all titles with torrent status merged in.

        Fetches titles from INI config and torrent status from the client,
        then merges torrent state/progress/name into each title by hash.
        """
        titles_data = cls.get_titles_logic()
        torrents_data = TorrentService.get_releases_torrent_status()

        torrents_dict = {}
        if hasattr(torrents_data, "data") and torrents_data.data:
            for torrent in torrents_data.data:
                if isinstance(torrent, dict) and torrent.get("hash"):
                    torrents_dict[torrent["hash"]] = torrent

        for title, data in titles_data.items():
            if not isinstance(data, dict):
                continue
            hash_value = data.get("hash")
            if hash_value in torrents_dict:
                t = torrents_dict[hash_value]
                data["torrent_info"] = {
                    "state": t.get("state"),
                    "progress": t.get("progress"),
                    "name": t.get("name"),
                }

        return titles_data

    @classmethod
    def get_torrents_logic(cls, query: str) -> Dict:
        """Search for torrents using query.
        If the API returns retry_suggested=True, retries once with the same query.
        If the retry still returns retry_suggested, returns an error payload with message.
        """
        if not query:
            return {}

        config = cls.initiate_config()
        config.args = query
        search_result = search_torrents(config)
        response = search_result.response

        if not isinstance(response, dict):
            return response

        if response.get("retry_suggested") is not True:
            return response

        # One automatic retry for this search action
        search_result = search_torrents(config)
        retry_response = search_result.response

        if not isinstance(retry_response, dict):
            return retry_response

        if retry_response.get("retry_suggested") is not True:
            return retry_response

        # Retry still suggested: do not retry again; return user-facing message
        message = retry_response.get("message") or "Please repeat the search."
        return {
            "error": True,
            "message": message,
            "results": [],
        }

    @classmethod
    def get_torrent_logic(cls, torrent_id: str) -> Dict:
        """Get specific torrent by ID."""
        if not torrent_id:
            return {}

        config = cls.initiate_config()
        config.args = torrent_id
        search_result = get_torrent_external(config)
        return search_result.response

    @classmethod
    def add_torrent_logic(cls, request: Any) -> Dict:
        """Add a new torrent."""
        if not request:
            return {}

        data = json.loads(request.data.decode("utf-8"))
        torrent_url = data.get("torrent_url")

        config = cls.initiate_config()
        config.args = RequestData(url=torrent_url)
        output = add_torrent_external(config)
        return cls.serialize_operation_result(output)

    @classmethod
    def add_release_logic(cls, request: Dict) -> Dict:
        """Add a new release."""
        try:
            config = cls.initiate_config()

            # Handle ongoing field (UI) -> partial (CLI arg for library)
            ongoing_value = request.get("ongoing", "true")
            is_partial = ongoing_value in ("true", "True", True, "1", 1)

            request_data = RequestData(
                url=request["url"],
                season=request["season"],
                index=int(request["index"]),
                correction=int(request["correction"]),
                title=request["title"],
                path=config.application_config.default_download_dir,
                partial=is_partial,
                release_group=request.get("release_group", ""),
                meta=request.get("meta", ""),
            )

            config.args = request_data
            operation_result = add_release_by_url(config)
            return cls.serialize_operation_result(operation_result)
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def update_release_logic(cls, request: Dict) -> Dict:
        """Update an existing release."""
        try:
            config = cls.initiate_config()
            request_data = RequestData(codename=request["codename"])
            config.args = request_data
            operation_result = update_release_by_name(config)
            return cls.serialize_operation_result(operation_result)
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def update_all_releases_logic(cls) -> Dict:
        """Update all releases."""
        try:
            config = cls.initiate_config()
            request_data = RequestData()
            config.args = request_data
            operation_result = update_releases(config)
            return cls.serialize_operation_result(operation_result)
        except Exception as e:
            return {"error": str(e)}

    @classmethod
    def serialize_operation_result(cls, operation_result: Any) -> Dict:
        """Serialize operation result to JSON-compatible format."""
        return {
            "operation_type": operation_result.operation_type.name
            if operation_result.operation_type
            else None,
            "torrent_references": [
                str(torrent) for torrent in operation_result.torrent_references
            ],
            "titles_references": [
                str(titles) for titles in operation_result.titles_references
            ],
            "status_message": operation_result.status_message,
            "response_code": operation_result.response_code.name
            if operation_result.response_code
            else None,
            "operation_logs": operation_result.operation_logs,
            "start_time": operation_result.start_time.isoformat()
            if operation_result.start_time
            else None,
            "end_time": operation_result.end_time.isoformat()
            if operation_result.end_time
            else None,
        }

    @classmethod
    def proxy_image_logic(cls, url: str) -> Response:
        """Proxy image requests through the server."""
        if not url:
            return Response("No URL provided", status=400)

        # Normalize the URL
        if url.startswith("//"):
            url = "https:" + url
        elif not url.startswith(("http://", "https://")):
            url = "https://" + url

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            response.raise_for_status()
            return Response(
                response.iter_content(chunk_size=1024),
                content_type=response.headers.get("Content-Type", "image/jpeg"),
            )
        except requests.RequestException as e:
            # Get status code if available, otherwise use 502 Bad Gateway
            status_code = (
                getattr(e.response, "status_code", 502)
                if hasattr(e, "response")
                else 502
            )
            return Response(f"Failed to fetch image: {str(e)}", status=status_code)


class StreamingService(BaseService):
    """Service for handling streaming site operations."""

    @classmethod
    def search_titles_from_streaming_site(cls, query: str) -> Dict:
        """Search for titles on streaming sites."""
        if not query:
            return {}
        main_logic = MainLogic()
        return main_logic.search_releases(query)

    @classmethod
    def get_streaming_site_release_details(
        cls, provider_name: str, release_url: str
    ) -> Dict:
        """Get detailed information about a streaming release."""
        main_logic = MainLogic()
        return main_logic.get_release_details(provider_name, release_url)


class SearchService(BaseService):
    """Service for handling multi-source search operations."""

    @classmethod
    def multi_search(cls, query: str) -> List[Dict]:
        """Search across multiple sources (MAL, TMDB, local DB)."""
        combined_data = []

        # Safe fetching function
        def safe_fetch(data: Dict, keys: List[str], default: Any = "") -> Any:
            try:
                for key in keys:
                    data = data[key]
                return data if data is not None else default
            except (KeyError, TypeError, IndexError):
                return default

        # Fetch data from various sources
        try:
            mal_data = MALService.search_anime(query)
        except Exception:
            mal_data = {"data": []}

        try:
            tmdb_data = TMDBService.search_media(query)
        except Exception:
            tmdb_data = {"results": []}

        try:
            localdb_data = DatabaseService.get_anime_by_name(query)
        except Exception:
            localdb_data = []

        # Process MAL data
        for item in mal_data.get("data", [])[:4]:
            alternatives = " | ".join(
                [
                    safe_fetch(item, ["node", "alternative_titles", "en"]),
                    safe_fetch(item, ["node", "alternative_titles", "ja"]),
                    " | ".join(
                        safe_fetch(item, ["node", "alternative_titles", "synonyms"], [])
                    ),
                ]
            )
            combined_data.append(
                {
                    "source": "MAL",
                    "title": safe_fetch(item, ["node", "title"]),
                    "id": safe_fetch(item, ["node", "id"]),
                    "status": safe_fetch(item, ["node", "status"]),
                    "mediaType": safe_fetch(item, ["node", "media_type"]),
                    "image": safe_fetch(item, ["node", "main_picture", "medium"]),
                    "description": safe_fetch(item, ["node", "title"]),
                    "releaseDate": safe_fetch(item, ["node", "start_date"]),
                    "alternative": alternatives,
                }
            )

        # Process TMDB data
        for item in tmdb_data.get("results", [])[:4]:
            item_id = item["id"]
            media_type = item.get("media_type", "Unknown")

            try:
                details = TMDBService.get_media_detail(item_id, media_type)
            except Exception:
                details = {}

            relevant_countries = ["JP", "US", "UA", "UK"]
            source_array = safe_fetch(
                details, ["alternative_titles", "results"]
            ) or safe_fetch(details, ["alternative_titles", "titles"])

            alternative_titles = " | ".join(
                title["title"]
                for title in source_array
                if title.get("iso_3166_1") in relevant_countries
            )

            alternative = (
                f"{safe_fetch(item, ['original_name'])} | {alternative_titles}"
                if "original_name" in item
                else alternative_titles
            )

            combined_data.append(
                {
                    "source": "TMDB",
                    "title": safe_fetch(item, ["name"]) or safe_fetch(item, ["title"]),
                    "id": item_id,
                    "status": safe_fetch(details, ["status"]) or "Unknown",
                    "mediaType": media_type,
                    "image": f"https://image.tmdb.org/t/p/w500{safe_fetch(item, ['poster_path'])}",
                    "description": safe_fetch(item, ["overview"]),
                    "releaseDate": safe_fetch(item, ["first_air_date"])
                    or safe_fetch(item, ["release_date"]),
                    "alternative": alternative,
                }
            )

        # Process localdb data
        for item in localdb_data[:4]:
            combined_data.append(
                {
                    "source": "localdb",
                    "title": safe_fetch(item, ["titleUa"]),
                    "id": item["id"],
                    "status": "Currently Airing"
                    if item.get("status_id") == 2
                    else "Finished Airing",
                    "mediaType": "Anime",
                    "image": "",
                    "description": safe_fetch(item, ["description"]),
                    "releaseDate": safe_fetch(item, ["releaseDate"]),
                    "alternative": safe_fetch(item, ["titleEn"]),
                }
            )

        return combined_data


class TorrentService(BaseService):
    """Service for handling torrent-related operations."""

    @classmethod
    def get_releases_torrent_status(cls) -> Dict:
        """Get status of all torrent releases."""
        config = TolokaService.initiate_config()
        category = config.app_config[config.application_config.client]["category"]
        tags = config.app_config[config.application_config.client]["tag"]

        return config.client.get_torrent_info(
            status_filter="all",
            category=category,
            tags=tags,
            sort="added_on",
            reverse=True,
        )
