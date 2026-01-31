import json

import pytest

from app.models.base import db
from app.models.user import User
from app.models.application_settings import ApplicationSettings


def _ensure_open_registration(app):
    with app.app_context():
        setting = ApplicationSettings.query.filter_by(key="open_registration").first()
        if setting is None:
            db.session.add(
                ApplicationSettings(
                    section="toloka2web",
                    key="open_registration",
                    value="True",
                )
            )
            db.session.commit()


def _create_user(app, username, password, roles="user"):
    with app.app_context():
        user = User(username=username, roles=roles)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.id


def _login_jwt(client, username, password):
    response = client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )
    assert response.status_code == 200
    return response.get_json()


def _login_session(client, username, password):
    response = client.post(
        "/login",
        data={"username": username, "password": password, "remember_me": "false"},
        headers={"Accept": "application/json"},
    )
    assert response.status_code == 200
    return response.get_json()


@pytest.fixture()
def api_key_headers():
    return {"X-API-Key": "test-api-key"}


def test_auth_endpoints_happy_path(app, client):
    _ensure_open_registration(app)

    with app.test_request_context(
        "/api/auth/register",
        method="POST",
        json={"username": "auth-user", "password": "strongpass"},
    ):
        from app.routes.auth import register

        register_response, status_code = register()
    assert status_code == 201
    assert register_response.get_json()["user"]["username"] == "auth-user"

    tokens = _login_jwt(client, "auth-user", "strongpass")
    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    me_response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert me_response.status_code == 200
    assert me_response.get_json()["username"] == "auth-user"

    validate_response = client.post(
        "/api/auth/validate",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert validate_response.status_code == 200
    assert validate_response.get_json()["valid"] is True

    refresh_response = client.post(
        "/api/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"},
    )
    assert refresh_response.status_code == 200
    assert refresh_response.get_json()["access_token"]

    logout_response = client.post(
        "/api/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert logout_response.status_code == 200

    tokens = _login_jwt(client, "auth-user", "strongpass")
    change_response = client.post(
        "/api/auth/change-password",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
        json={"current_password": "strongpass", "new_password": "newpass123"},
    )
    assert change_response.status_code == 200


def test_profile_and_admin_user_endpoints(app, client, api_key_headers):
    user_id = _create_user(app, "profile-user", "password123", roles="user")
    _create_user(app, "admin-user", "adminpass123", roles="admin")

    tokens = _login_jwt(client, "profile-user", "password123")
    update_response = client.put(
        "/api/profile",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
        json={"username": "profile-user-updated"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["user"]["username"] == "profile-user-updated"

    profile_response = client.get(
        "/api/profile",
        headers={"Authorization": f"Bearer {tokens['access_token']}"},
    )
    assert profile_response.status_code == 200
    assert profile_response.get_json()["username"] == "profile-user"

    list_response = client.get("/api/users", headers=api_key_headers)
    assert list_response.status_code == 200
    assert any(user["username"] == "admin-user" for user in list_response.get_json())

    update_user_response = client.put(
        f"/api/users/{user_id}",
        headers=api_key_headers,
        json={"roles": "admin"},
    )
    assert update_user_response.status_code == 200
    assert update_user_response.get_json()["user"]["roles"] == "admin"

    deletable_id = _create_user(app, "delete-user", "deletepass123", roles="user")
    delete_response = client.delete(
        f"/api/users/{deletable_id}",
        headers=api_key_headers,
    )
    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "User deleted successfully"


def test_settings_endpoints(app, client, api_key_headers, monkeypatch):
    _create_user(app, "settings-admin", "adminpass123", roles="admin")
    _login_session(client, "settings-admin", "adminpass123")

    monkeypatch.setattr(
        "app.services.config_service.ConfigService.read_all_settings_from_db",
        lambda: [{"section": "toloka2web", "key": "open_registration", "value": "True"}],
    )
    monkeypatch.setattr(
        "app.services.config_service.ConfigService.add_new_setting",
        lambda section, key, value: {"section": section, "key": key, "value": value},
    )

    list_response = client.get("/api/settings", headers=api_key_headers)
    assert list_response.status_code == 200
    assert list_response.get_json()[0]["key"] == "open_registration"

    add_response = client.post(
        "/api/settings",
        headers=api_key_headers,
        json={"section": "toloka2web", "key": "new_key", "value": "new"},
    )
    assert add_response.status_code == 200
    assert add_response.get_json()["key"] == "new_key"

    monkeypatch.setattr(
        "app.services.config_service.ConfigService.update_setting",
        lambda *_args, **_kwargs: {"updated": True},
    )
    update_response = client.post(
        "/api/settings/1",
        data={"section": "toloka2web", "key": "open_registration", "value": "False"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["updated"] is True

    monkeypatch.setattr(
        "app.services.config_service.ConfigService.sync_settings",
        lambda *_args, **_kwargs: {"synced": True},
    )
    sync_response = client.post(
        "/api/settings/sync",
        data={"direction": "to", "type": "app"},
    )
    assert sync_response.status_code == 200
    assert sync_response.get_json()["synced"] is True

    monkeypatch.setattr(
        "app.services.route_service.RouteService.get_installed_packages",
        lambda: {"flask": "3.0.0"},
    )
    versions_response = client.get("/api/settings/versions")
    assert versions_response.status_code == 200
    assert versions_response.get_json()["flask"] == "3.0.0"

    monkeypatch.setattr(
        "app.services.route_service.RouteService.list_files",
        lambda _path: {"files": []},
    )
    files_response = client.get("/api/settings/files")
    assert files_response.status_code == 200
    assert files_response.get_json()["files"] == []


def test_anime_and_studio_endpoints(app, client, api_key_headers, monkeypatch):
    _create_user(app, "anime-user", "password123", roles="user")
    _login_session(client, "anime-user", "password123")

    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.list_all_anime",
        lambda: [{"id": 1, "title": "Demo"}],
    )
    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.get_anime_by_id",
        lambda _anime_id: {"id": 1, "title": "Demo"},
    )
    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.get_related_animes",
        lambda _anime_id: [{"id": 2, "title": "Related"}],
    )
    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.get_studios_by_anime_id",
        lambda _anime_id: [{"id": 10, "name": "Studio"}],
    )
    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.list_all_studios",
        lambda: [{"id": 10, "name": "Studio"}],
    )
    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.search_studio_by_id",
        lambda _studio_id: {"id": 10, "name": "Studio"},
    )
    monkeypatch.setattr(
        "app.services.services_db.DatabaseService.get_anime_by_studio_id",
        lambda _studio_id: [{"id": 1, "title": "Demo"}],
    )

    list_anime_response = client.get("/api/anime", headers=api_key_headers)
    assert list_anime_response.status_code == 200
    assert list_anime_response.get_json()[0]["title"] == "Demo"

    detail_response = client.get("/api/anime/1", headers=api_key_headers)
    assert detail_response.status_code == 200
    assert detail_response.get_json()["id"] == 1

    related_response = client.get("/api/anime/1/related")
    assert related_response.status_code == 200
    assert related_response.get_json()[0]["id"] == 2

    studios_response = client.get("/api/anime/1/studios")
    assert studios_response.status_code == 200
    assert studios_response.get_json()[0]["name"] == "Studio"

    list_studios_response = client.get("/api/studio", headers=api_key_headers)
    assert list_studios_response.status_code == 200
    assert list_studios_response.get_json()[0]["id"] == 10

    studio_detail_response = client.get("/api/studio/10", headers=api_key_headers)
    assert studio_detail_response.status_code == 200
    assert studio_detail_response.get_json()["name"] == "Studio"

    studio_anime_response = client.get("/api/studio/10/anime", headers=api_key_headers)
    assert studio_anime_response.status_code == 200
    assert studio_anime_response.get_json()[0]["title"] == "Demo"


def test_release_endpoints(client, api_key_headers, monkeypatch):
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_titles_with_torrent_status",
        lambda: {"release": {"title": "Release"}},
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.add_release_logic",
        lambda _data: {"response_code": "SUCCESS", "operation_type": "ADD"},
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.update_release_logic",
        lambda _data: {"response_code": "SUCCESS", "operation_type": "UPDATE"},
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.update_all_releases_logic",
        lambda: {"response_code": "SUCCESS", "operation_type": "UPDATE_ALL"},
    )
    monkeypatch.setattr(
        "app.services.services.TorrentService.get_releases_torrent_status",
        lambda: [{"hash": "abc"}],
    )
    monkeypatch.setattr(
        "app.services.config_service.ConfigService.get_release_defaults",
        lambda: {"default_meta": "meta"},
    )
    monkeypatch.setattr(
        "app.services.config_service.ConfigService.edit_release",
        lambda _data: "edited",
    )
    monkeypatch.setattr(
        "app.services.config_service.ConfigService.delete_release",
        lambda _data: "deleted",
    )

    list_response = client.get("/api/releases", headers=api_key_headers)
    assert list_response.status_code == 200
    assert list_response.get_json()["release"]["title"] == "Release"

    add_response = client.post(
        "/api/releases",
        headers=api_key_headers,
        json={"url": "https://toloka.to/t1"},
    )
    assert add_response.status_code == 200
    assert add_response.get_json()["operation_type"] == "ADD"

    update_response = client.post(
        "/api/releases/update",
        headers=api_key_headers,
        json={"codename": "release"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["operation_type"] == "UPDATE"

    update_all_response = client.post(
        "/api/releases/update",
        headers=api_key_headers,
    )
    assert update_all_response.status_code == 200
    assert update_all_response.get_json()["operation_type"] == "UPDATE_ALL"

    torrents_response = client.get("/api/releases/torrents", headers=api_key_headers)
    assert torrents_response.status_code == 200
    assert "abc" in torrents_response.get_data(as_text=True)

    defaults_response = client.get("/api/releases/defaults", headers=api_key_headers)
    assert defaults_response.status_code == 200
    assert defaults_response.get_json()["default_meta"] == "meta"

    detail_response = client.get("/api/releases/abc", headers=api_key_headers)
    assert detail_response.status_code == 200
    assert detail_response.get_json()["msg"] == "abc"

    edit_response = client.put(
        "/api/releases",
        headers=api_key_headers,
        json={"codename": "release"},
    )
    assert edit_response.status_code == 200
    assert edit_response.get_json()["msg"] == "edited"

    delete_response = client.delete(
        "/api/releases",
        headers=api_key_headers,
        json={"codename": "release"},
    )
    assert delete_response.status_code == 200
    assert delete_response.get_json()["msg"] == "deleted"


def test_stream_mal_tmdb_toloka_endpoints(client, api_key_headers, monkeypatch):
    monkeypatch.setattr(
        "app.services.services.StreamingService.search_titles_from_streaming_site",
        lambda _query: {"results": [{"title": "Stream"}]},
    )
    monkeypatch.setattr(
        "app.services.services.StreamingService.add_title_from_streaming_site",
        lambda _data: {"added": True},
        raising=False,
    )
    monkeypatch.setattr(
        "app.services.services.StreamingService.get_streaming_site_release_details",
        lambda _provider, _link: {"detail": "info"},
    )
    monkeypatch.setattr(
        "app.services.mal_service.MALService.search_anime",
        lambda _query: {"results": [{"title": "MAL"}]},
    )
    monkeypatch.setattr(
        "app.services.mal_service.MALService.get_anime_detail",
        lambda _anime_id: {"id": 1, "title": "MAL"},
    )
    monkeypatch.setattr(
        "app.services.tmdb_service.TMDBService.search_media",
        lambda _query: {"results": [{"title": "TMDB"}]},
    )
    monkeypatch.setattr(
        "app.services.tmdb_service.TMDBService.get_media_detail",
        lambda _id, _media_type: {"id": 2, "title": "TMDB"},
    )
    monkeypatch.setattr(
        "app.services.tmdb_service.TMDBService.get_trending_by_type",
        lambda _media_type: {"results": [{"title": "Trend"}]},
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_torrents_logic",
        lambda _query: {"results": [{"id": "rel"}]},
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_torrent_logic",
        lambda _release_id: {"id": "rel"},
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.add_torrent_logic",
        lambda _request: {"added": True},
    )

    stream_response = client.get("/api/stream?query=demo", headers=api_key_headers)
    assert stream_response.status_code == 200
    assert json.loads(stream_response.get_data(as_text=True))["results"][0]["title"] == "Stream"

    add_stream_response = client.post(
        "/api/stream",
        headers=api_key_headers,
        json={"provider": "demo", "link": "https://example.com"},
    )
    assert add_stream_response.status_code == 200
    assert add_stream_response.get_json()["added"] is True

    details_response = client.post(
        "/api/stream/details",
        headers=api_key_headers,
        json={"provider": "demo", "link": "https://example.com"},
    )
    assert details_response.status_code == 200
    assert json.loads(details_response.get_data(as_text=True))["detail"] == "info"

    mal_response = client.get("/api/mal/search?query=demo", headers=api_key_headers)
    assert mal_response.status_code == 200
    assert mal_response.get_json()["results"][0]["title"] == "MAL"

    mal_detail_response = client.get("/api/mal/detail/1", headers=api_key_headers)
    assert mal_detail_response.status_code == 200
    assert mal_detail_response.get_json()["title"] == "MAL"

    tmdb_response = client.get("/api/tmdb/search?query=demo", headers=api_key_headers)
    assert tmdb_response.status_code == 200
    assert tmdb_response.get_json()["results"][0]["title"] == "TMDB"

    tmdb_detail_response = client.get(
        "/api/tmdb/detail/2?type=movie",
        headers=api_key_headers,
    )
    assert tmdb_detail_response.status_code == 200
    assert tmdb_detail_response.get_json()["title"] == "TMDB"

    trending_response = client.get("/api/tmdb/trending?type=movie")
    assert trending_response.status_code == 200
    assert trending_response.get_json()["results"][0]["title"] == "Trend"

    toloka_response = client.get("/api/toloka?query=demo", headers=api_key_headers)
    assert toloka_response.status_code == 200
    assert toloka_response.get_json()["results"][0]["id"] == "rel"

    toloka_detail_response = client.get("/api/toloka/rel", headers=api_key_headers)
    assert toloka_detail_response.status_code == 200
    assert toloka_detail_response.get_json()["id"] == "rel"

    toloka_add_response = client.post(
        "/api/toloka",
        headers=api_key_headers,
        json={"release_id": "rel"},
    )
    assert toloka_add_response.status_code == 200
    assert toloka_add_response.get_json()["added"] is True


def test_search_auth_check_and_image_endpoints(app, client, api_key_headers, monkeypatch):
    _create_user(app, "search-user", "password123", roles="user")
    _login_session(client, "search-user", "password123")

    monkeypatch.setattr(
        "app.services.services.SearchService.multi_search",
        lambda _query: {"results": ["item"]},
    )
    search_response = client.get("/api/search?query=demo")
    assert search_response.status_code == 200
    assert search_response.get_json()["results"][0] == "item"

    auth_check_response = client.get("/api/auth/check", headers=api_key_headers)
    assert auth_check_response.status_code == 200
    assert auth_check_response.get_json()["auth_type"] == "session"

    monkeypatch.setattr(
        "app.services.services.TolokaService.proxy_image_logic",
        lambda _url: b"image-bytes",
    )
    image_response = client.get("/api/image?url=https://example.com")
    assert image_response.status_code == 200
    assert image_response.get_data() == b"image-bytes"
