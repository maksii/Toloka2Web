import datetime
import types

from app.models.releases import Releases
from app.services.config_service import ConfigService
from app.services.services import TolokaService


def test_add_release_flow(client, monkeypatch):
    def _fake_add_release(request_data):
        return {
            "operation_type": "ADD_RELEASE",
            "status_message": "release added",
            "response_code": "SUCCESS",
        }

    monkeypatch.setattr(TolokaService, "add_release_logic", _fake_add_release)

    response = client.post(
        "/api/releases",
        headers={"X-API-Key": "test-api-key"},
        json={
            "url": "https://toloka.to/t123456",
            "season": "1",
            "index": 1,
            "correction": 0,
            "title": "Demo release",
            "ongoing": "true",
        },
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["operation_type"] == "ADD_RELEASE"
    assert payload["response_code"] == "SUCCESS"


def test_update_release_flow_success(client, monkeypatch):
    def _fake_update_release(request_data):
        return {
            "operation_type": "UPDATE_RELEASE",
            "status_message": "release updated",
            "response_code": "SUCCESS",
        }

    monkeypatch.setattr(TolokaService, "update_release_logic", _fake_update_release)

    response = client.post(
        "/api/releases/update",
        headers={"X-API-Key": "test-api-key"},
        json={"codename": "release-code"},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["operation_type"] == "UPDATE_RELEASE"
    assert payload["response_code"] == "SUCCESS"


def test_update_release_flow_force_flag(client, monkeypatch):
    captured = {}

    def _fake_update_release(request_data):
        captured["force"] = request_data.get("force")
        return {
            "operation_type": "UPDATE_RELEASE",
            "status_message": "release force updated",
            "response_code": "SUCCESS",
        }

    monkeypatch.setattr(TolokaService, "update_release_logic", _fake_update_release)

    response = client.post(
        "/api/releases/update",
        headers={"X-API-Key": "test-api-key"},
        json={"codename": "release-code", "force": True},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["operation_type"] == "UPDATE_RELEASE"
    assert payload["response_code"] == "SUCCESS"
    assert captured["force"] is True


def test_update_release_flow_same_date_failure(client, monkeypatch):
    def _fake_update_release(request_data):
        return {
            "error": "release already updated on same date",
        }

    monkeypatch.setattr(TolokaService, "update_release_logic", _fake_update_release)

    response = client.post(
        "/api/releases/update",
        headers={"X-API-Key": "test-api-key"},
        json={"codename": "release-code"},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["error"] == "release already updated on same date"


def test_update_release_flow_qbit_failure(client, monkeypatch):
    def _fake_update_release(request_data):
        return {
            "operation_type": "UPDATE_RELEASE",
            "status_message": "torrent not started in the end phase",
            "response_code": "FAILED",
        }

    monkeypatch.setattr(TolokaService, "update_release_logic", _fake_update_release)

    response = client.post(
        "/api/releases/update",
        headers={"X-API-Key": "test-api-key"},
        json={"codename": "release-code"},
    )
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status_message"] == "torrent not started in the end phase"
    assert payload["response_code"] == "FAILED"


def test_update_release_logic_force_argument(monkeypatch):
    captured = {}

    def _fake_update_release_by_name(config):
        captured["codename"] = config.args.codename
        captured["force"] = config.args.force
        return types.SimpleNamespace(
            operation_type=types.SimpleNamespace(name="UPDATE_RELEASE"),
            torrent_references=[],
            titles_references=[],
            status_message="force update",
            response_code=types.SimpleNamespace(name="SUCCESS"),
            operation_logs=[],
            start_time=None,
            end_time=None,
        )

    monkeypatch.setattr(
        TolokaService, "initiate_config", lambda: types.SimpleNamespace()
    )
    monkeypatch.setattr(
        "app.services.services.update_release_by_name", _fake_update_release_by_name
    )

    result = TolokaService.update_release_logic(
        {"codename": "release-code", "force": "true"}
    )

    assert result["response_code"] == "SUCCESS"
    assert captured["codename"] == "release-code"
    assert captured["force"] is True


def test_edit_release_accepts_full_year(app):
    form = {
        "codename": "demo-release",
        "episode_index": "1",
        "season_number": "1",
        "torrent_name": "Demo Torrent",
        "download_dir": "/downloads",
        "publish_date": "2026-01-28 22:21",
        "release_group": "Group",
        "meta": "WEBDL",
        "hash": "deadbeef",
        "adjusted_episode_number": "1",
        "guid": "12345",
        "ongoing": "true",
    }

    with app.app_context():
        ConfigService.edit_release(form)
        release = Releases.query.filter_by(section="demo-release").first()

    assert release is not None
    assert release.publish_date == datetime.datetime(2026, 1, 28, 22, 21)
