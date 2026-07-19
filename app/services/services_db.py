"""Anime catalog service backed by the CPRcatalog JSON exports.

Data source: https://github.com/DrBryanMan/CPRcatalog (json/ directory) — a
catalog of Ukrainian fandub/fansub anime releases exported from Notion.
The three JSON files (titles, releases, teams) are downloaded to data/ and
served from memory. IDs are Notion UUID strings.
"""

import json
import logging
import os
import threading
from typing import Dict, List, Optional

import requests

from app.services.base_service import BaseService

CATALOG_BASE_URL = "https://raw.githubusercontent.com/DrBryanMan/CPRcatalog/main/json/"
CATALOG_FILES = {
    "titles": "AnimeTitlesDB.json",
    "releases": "AnimeReleasesDB.json",
    "teams": "TeamsDB.json",
}
DATA_DIR = "data"


class DatabaseService(BaseService):
    """Serves anime/studio data from the CPRcatalog JSON catalog.

    Keeps the public API of the old SQLite-backed service so routes,
    aggregated search and the frontend contracts stay stable. "Studios"
    map to CPRcatalog fandub teams.
    """

    _lock = threading.Lock()
    _loaded = False

    _titles: Dict[str, dict] = {}
    _teams: Dict[str, dict] = {}
    _releases_by_anime: Dict[str, list] = {}
    _team_ids_by_anime: Dict[str, list] = {}
    _anime_ids_by_team: Dict[str, list] = {}

    # --- loading -----------------------------------------------------------

    @classmethod
    def initialize_database(cls) -> None:
        """Load the catalog from disk into memory (downloads it if missing)."""
        with cls._lock:
            cls._load_locked()

    @classmethod
    def _ensure_loaded(cls) -> None:
        if cls._loaded:
            return
        with cls._lock:
            if not cls._loaded:
                cls._load_locked()

    @classmethod
    def _load_locked(cls) -> None:
        if any(
            not os.path.exists(os.path.join(DATA_DIR, f))
            for f in CATALOG_FILES.values()
        ):
            try:
                cls._download()
            except Exception as e:
                logging.warning(f"Failed to download anime catalog: {e}")

        data = {}
        for key, filename in CATALOG_FILES.items():
            path = os.path.join(DATA_DIR, filename)
            try:
                with open(path, encoding="utf-8") as f:
                    data[key] = json.load(f)
            except (OSError, ValueError) as e:
                logging.warning(f"Failed to load catalog file {path}: {e}")
                data[key] = []
        cls._index(data["titles"], data["releases"], data["teams"])
        cls._loaded = True

    @classmethod
    def _download(cls) -> None:
        os.makedirs(DATA_DIR, exist_ok=True)
        for filename in CATALOG_FILES.values():
            response = requests.get(CATALOG_BASE_URL + filename, timeout=120)
            response.raise_for_status()
            json.loads(response.content)  # validate before overwriting local copy
            path = os.path.join(DATA_DIR, filename)
            # atomic replace: a killed process must not leave a truncated file
            with open(path + ".tmp", "wb") as f:
                f.write(response.content)
            os.replace(path + ".tmp", path)

    @classmethod
    def _index(cls, titles: list, releases: list, teams: list) -> None:
        cls._titles = {t["id"]: t for t in titles if t.get("id")}
        cls._teams = {t["id"]: t for t in teams if t.get("id")}

        releases_by_anime: Dict[str, list] = {}
        team_ids_by_anime: Dict[str, list] = {}
        anime_ids_by_team: Dict[str, list] = {}
        for release in releases:
            release_teams = list(release.get("teams") or []) + list(
                release.get("teamscolab") or []
            )
            for anime_id in release.get("animeIds") or []:
                releases_by_anime.setdefault(anime_id, []).append(release)
                anime_teams = team_ids_by_anime.setdefault(anime_id, [])
                for team_id in release_teams:
                    if team_id not in anime_teams:
                        anime_teams.append(team_id)
                    team_animes = anime_ids_by_team.setdefault(team_id, [])
                    if anime_id not in team_animes:
                        team_animes.append(anime_id)
        cls._releases_by_anime = releases_by_anime
        cls._team_ids_by_anime = team_ids_by_anime
        cls._anime_ids_by_team = anime_ids_by_team

    # --- serialization (legacy field contract) -----------------------------

    @staticmethod
    def _clean(value):
        """The catalog exporter emits literal "None" strings for missing values."""
        return None if value in (None, "", "None") else value

    @classmethod
    def _anime_dict(cls, title: dict) -> Dict:
        return {
            "id": title["id"],
            "titleUa": title.get("title"),
            "titleEn": title.get("romaji"),
            "synonyms": title.get("synonyms") or [],
            "releaseDate": cls._clean(title.get("year")),
            "season": title.get("season"),
            "episodes": cls._clean(title.get("episodes")),
            "malId": title.get("mal_id"),
            "poster": title.get("poster") or title.get("hikka_poster"),
            "hikkaUrl": title.get("hikka_url"),
            "type": {"name": title.get("format")},
            "status": {"name": title.get("status")},
        }

    @staticmethod
    def _studio_dict(team: dict) -> Dict:
        return {
            "id": team["id"],
            "name": team.get("name"),
            "altname": team.get("altname") or [],
            "telegram": team.get("tg"),
            "site": team.get("site"),
            "logo": team.get("logo"),
            "status": team.get("status"),
        }

    @classmethod
    def _release_dict(cls, release: dict) -> Dict:
        team_ids = list(release.get("teams") or []) + list(
            release.get("teamscolab") or []
        )
        return {
            "id": release["id"],
            "title": release.get("title"),
            "teams": [
                {"id": tid, "name": (cls._teams.get(tid) or {}).get("name")}
                for tid in team_ids
            ],
            "status": release.get("status"),
            "episodes": release.get("episodes"),
            "dubinfo": release.get("dubinfo") or [],
            "subinfo": release.get("subinfo") or [],
            "torrentLinks": [
                link for link in release.get("torrentLinks") or [] if link.get("href")
            ],
            "fexlink": release.get("fexlink"),
            "sitelink": release.get("sitelink"),
        }

    # --- reads -------------------------------------------------------------

    @classmethod
    def get_anime_by_id(cls, anime_id: str) -> Optional[Dict]:
        """Get anime by ID."""
        cls._ensure_loaded()
        title = cls._titles.get(anime_id)
        return cls._anime_dict(title) if title else None

    @classmethod
    def get_anime_by_name(cls, partial_name: str) -> List[Dict]:
        """Search anime by partial name match (title, romaji, synonyms)."""
        cls._ensure_loaded()
        needle = (partial_name or "").lower()
        results = []
        for title in cls._titles.values():
            names = [title.get("title"), title.get("romaji")]
            names += title.get("synonyms") or []
            names += title.get("hikkaSynonyms") or []
            if any(needle in name.lower() for name in names if name):
                results.append(cls._anime_dict(title))
        return results

    @classmethod
    def get_related_animes(cls, anime_id: str) -> List[Dict]:
        """Get related animes (relations + franchise) for a given anime ID."""
        cls._ensure_loaded()
        title = cls._titles.get(anime_id)
        if not title:
            return []
        related_ids = []
        for ref in (title.get("relations") or []) + (title.get("franchise") or []):
            ref_id = ref.get("id") if isinstance(ref, dict) else ref
            if ref_id and ref_id != anime_id and ref_id not in related_ids:
                related_ids.append(ref_id)
        return [
            cls._anime_dict(cls._titles[ref_id])
            for ref_id in related_ids
            if ref_id in cls._titles
        ]

    @classmethod
    def list_all_anime(cls) -> List[Dict]:
        """Get all anime."""
        cls._ensure_loaded()
        return [cls._anime_dict(t) for t in cls._titles.values()]

    @classmethod
    def list_all_studios(cls) -> List[Dict]:
        """Get all studios (fandub teams)."""
        cls._ensure_loaded()
        return [cls._studio_dict(t) for t in cls._teams.values()]

    @classmethod
    def search_studio_by_name(cls, partial_name: str) -> List[Dict]:
        """Search studios by partial name match (name + alternative names)."""
        cls._ensure_loaded()
        needle = (partial_name or "").lower()
        results = []
        for team in cls._teams.values():
            names = [team.get("name")] + (team.get("altname") or [])
            if any(needle in name.lower() for name in names if name):
                results.append(cls._studio_dict(team))
        return results

    @classmethod
    def search_studio_by_id(cls, studio_id: str) -> Optional[Dict]:
        """Get studio by ID."""
        cls._ensure_loaded()
        team = cls._teams.get(studio_id)
        return cls._studio_dict(team) if team else None

    @classmethod
    def get_studios_by_anime_id(cls, anime_id: str) -> List[Dict]:
        """Get all studios that released a given anime."""
        cls._ensure_loaded()
        return [
            cls._studio_dict(cls._teams[team_id])
            for team_id in cls._team_ids_by_anime.get(anime_id, [])
            if team_id in cls._teams
        ]

    @classmethod
    def get_anime_by_studio_id(cls, studio_id: str) -> List[Dict]:
        """Get all anime released by a given studio."""
        cls._ensure_loaded()
        return [
            cls._anime_dict(cls._titles[anime_id])
            for anime_id in cls._anime_ids_by_team.get(studio_id, [])
            if anime_id in cls._titles
        ]

    @classmethod
    def get_releases_by_anime_id(cls, anime_id: str) -> List[Dict]:
        """Get all fandub releases (with torrent links) for a given anime."""
        cls._ensure_loaded()
        return [cls._release_dict(r) for r in cls._releases_by_anime.get(anime_id, [])]

    # --- update ------------------------------------------------------------

    @classmethod
    def update_database(cls) -> Dict[str, str]:
        """Refresh the local catalog from the CPRcatalog GitHub repo."""
        try:
            with cls._lock:
                cls._download()
                cls._load_locked()
            return {
                "status": "success",
                "message": "Catalog has been updated successfully.",
            }
        except requests.RequestException as e:
            return {
                "status": "error",
                "message": f"Failed to download the catalog: {str(e)}",
            }
        except Exception as e:
            return {"status": "error", "message": f"An error occurred: {str(e)}"}
