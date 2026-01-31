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
