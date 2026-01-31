from app.models.base import db
from app.models.user import User


def _create_user(app, username, password, roles="admin"):
    with app.app_context():
        user = User(username=username, roles=roles)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.id


def test_mocked_release_and_toloka_flow(app, client, monkeypatch):
    _create_user(app, "flow-admin", "adminpass123", roles="admin")

    def _fake_add_release(request_data):
        return {
            "operation_type": "ADD_RELEASE",
            "status_message": "release added",
            "response_code": "SUCCESS",
        }

    def _fake_update_release(request_data):
        return {
            "operation_type": "UPDATE_RELEASE",
            "status_message": "release updated",
            "response_code": "SUCCESS",
        }

    def _fake_get_titles():
        return {"demo": {"title": "Example"}}

    def _fake_toloka_search(_query):
        return {"results": [{"id": "demo"}]}

    def _fake_toloka_get(_release_id):
        return {"id": "demo", "title": "Example"}

    monkeypatch.setattr(
        "app.services.services.TolokaService.add_release_logic",
        _fake_add_release,
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.update_release_logic",
        _fake_update_release,
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_titles_with_torrent_status",
        _fake_get_titles,
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_torrents_logic",
        _fake_toloka_search,
    )
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_torrent_logic",
        _fake_toloka_get,
    )

    add_response = client.post(
        "/api/releases",
        headers={"X-API-Key": "test-api-key"},
        json={"url": "https://toloka.to/t1"},
    )
    assert add_response.status_code == 200
    assert add_response.get_json()["response_code"] == "SUCCESS"

    update_response = client.post(
        "/api/releases/update",
        headers={"X-API-Key": "test-api-key"},
        json={"codename": "demo"},
    )
    assert update_response.status_code == 200
    assert update_response.get_json()["operation_type"] == "UPDATE_RELEASE"

    list_response = client.get("/api/releases", headers={"X-API-Key": "test-api-key"})
    assert list_response.status_code == 200
    assert list_response.get_json()["demo"]["title"] == "Example"

    toloka_search_response = client.get(
        "/api/toloka?query=demo",
        headers={"X-API-Key": "test-api-key"},
    )
    assert toloka_search_response.status_code == 200
    assert toloka_search_response.get_json()["results"][0]["id"] == "demo"

    toloka_detail_response = client.get(
        "/api/toloka/demo",
        headers={"X-API-Key": "test-api-key"},
    )
    assert toloka_detail_response.status_code == 200
    assert toloka_detail_response.get_json()["title"] == "Example"
