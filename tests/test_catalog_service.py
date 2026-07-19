"""Tests for the CPRcatalog-backed DatabaseService."""

import json

import pytest

import app.services.services_db as services_db
from app.services.services_db import DatabaseService

TITLES = [
    {
        "id": "title-1",
        "title": "Щаслива Зірка",
        "romaji": "Lucky Star",
        "synonyms": ["Lucky☆Star"],
        "hikkaSynonyms": ["Raki Suta"],
        "type": "Аніме",
        "format": "ТБ",
        "year": "2007",
        "status": "finished",
        "season": "spring",
        "episodes": "24",
        "mal_id": 1887,
        "poster": "https://example.com/poster.webp",
        "hikka_url": "https://hikka.io/anime/luckystar",
        "relations": [{"id": "title-2"}],
        "franchise": [],
    },
    {
        "id": "title-2",
        "title": "Щаслива Зірка OVA",
        "romaji": "Lucky Star OVA",
        "year": "None",
        "episodes": "None",
        "relations": [{"id": "title-1"}],
    },
]

RELEASES = [
    {
        "id": "release-1",
        "title": "Щаслива Зірка",
        "animeIds": ["title-1"],
        "teams": ["team-1"],
        "teamscolab": ["team-2"],
        "dubinfo": ["х2 голоса"],
        "subinfo": ["Софтсаб"],
        "status": "Завершено",
        "episodes": "24 / 24",
        "torrentLinks": [
            {"text": "WEBRip 1080p", "href": "https://toloka.to/t1"},
            {"text": "dead", "href": None},
        ],
        "fexlink": None,
        "sitelink": None,
    }
]

TEAMS = [
    {
        "id": "team-1",
        "name": "Шалене чаювання",
        "altname": ["Studio Sengoku"],
        "tg": "https://t.me/team1",
        "status": "Активна",
    },
    {"id": "team-2", "name": "Другa команда", "altname": []},
]


@pytest.fixture()
def catalog(tmp_path, monkeypatch):
    for filename, data in [
        (services_db.CATALOG_FILES["titles"], TITLES),
        (services_db.CATALOG_FILES["releases"], RELEASES),
        (services_db.CATALOG_FILES["teams"], TEAMS),
    ]:
        (tmp_path / filename).write_text(json.dumps(data), encoding="utf-8")
    monkeypatch.setattr(services_db, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(DatabaseService, "_loaded", False)
    yield
    DatabaseService._loaded = False


def test_anime_reads(catalog):
    anime = DatabaseService.get_anime_by_id("title-1")
    assert anime["titleUa"] == "Щаслива Зірка"
    assert anime["titleEn"] == "Lucky Star"
    assert anime["releaseDate"] == "2007"
    assert anime["type"]["name"] == "ТБ"
    assert anime["status"]["name"] == "finished"
    assert anime["malId"] == 1887

    # literal "None" strings from the catalog exporter are normalized to null
    ova = DatabaseService.get_anime_by_id("title-2")
    assert ova["releaseDate"] is None
    assert ova["episodes"] is None

    assert DatabaseService.get_anime_by_id("missing") is None
    assert len(DatabaseService.list_all_anime()) == 2

    # search matches title, romaji and synonyms, case-insensitive
    assert len(DatabaseService.get_anime_by_name("lucky")) == 2
    assert len(DatabaseService.get_anime_by_name("Зірка")) == 2
    assert len(DatabaseService.get_anime_by_name("raki")) == 1
    assert DatabaseService.get_anime_by_name("nope") == []

    related = DatabaseService.get_related_animes("title-1")
    assert [r["id"] for r in related] == ["title-2"]


def test_studio_reads(catalog):
    assert len(DatabaseService.list_all_studios()) == 2

    studio = DatabaseService.search_studio_by_id("team-1")
    assert studio["name"] == "Шалене чаювання"
    assert studio["telegram"] == "https://t.me/team1"
    assert DatabaseService.search_studio_by_id("missing") is None

    # search by name and altname
    assert len(DatabaseService.search_studio_by_name("чаювання")) == 1
    assert len(DatabaseService.search_studio_by_name("sengoku")) == 1

    # anime <-> studio relations go through releases (incl. collabs)
    studios = DatabaseService.get_studios_by_anime_id("title-1")
    assert {s["id"] for s in studios} == {"team-1", "team-2"}
    animes = DatabaseService.get_anime_by_studio_id("team-2")
    assert [a["id"] for a in animes] == ["title-1"]


def test_releases_read(catalog):
    releases = DatabaseService.get_releases_by_anime_id("title-1")
    assert len(releases) == 1
    release = releases[0]
    assert release["status"] == "Завершено"
    assert {t["name"] for t in release["teams"]} == {"Шалене чаювання", "Другa команда"}
    # torrent links without href are dropped
    assert release["torrentLinks"] == [
        {"text": "WEBRip 1080p", "href": "https://toloka.to/t1"}
    ]
    assert DatabaseService.get_releases_by_anime_id("missing") == []
