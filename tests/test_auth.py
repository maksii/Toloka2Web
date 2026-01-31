import pytest

from app.models.base import db
from app.models.user import User
from app.routes.auth import register


def test_user_registration_and_login(app, client):
    with app.test_request_context(
        "/api/auth/register",
        method="POST",
        json={"username": "new-user", "password": "securepass"},
    ):
        register_response, status_code = register()

    assert status_code == 201
    register_payload = register_response.get_json()
    assert register_payload["user"]["username"] == "new-user"
    assert register_payload["user"]["roles"] == "admin"

    login_response = client.post(
        "/api/auth/login",
        json={"username": "new-user", "password": "securepass"},
    )
    assert login_response.status_code == 200
    login_payload = login_response.get_json()
    assert login_payload["access_token"]
    assert login_payload["refresh_token"]


@pytest.fixture()
def existing_user(app):
    with app.app_context():
        user = User(username="tester", roles="user")
        user.set_password("password123")
        db.session.add(user)
        db.session.commit()
        return user


@pytest.fixture()
def admin_user(app):
    with app.app_context():
        user = User(username="admin", roles="admin")
        user.set_password("adminpass123")
        db.session.add(user)
        db.session.commit()
        return user


def _get_access_token(client, username, password):
    response = client.post(
        "/api/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.get_json()["access_token"]


def test_api_access_with_jwt(client, existing_user, monkeypatch):
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_titles_with_torrent_status",
        lambda: {"demo": {"title": "example"}},
    )

    token = _get_access_token(client, "tester", "password123")
    response = client.get("/api/releases", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["demo"]["title"] == "example"


def test_api_access_with_session(client, existing_user, monkeypatch):
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_titles_with_torrent_status",
        lambda: {"demo": {"title": "example"}},
    )

    login_response = client.post(
        "/login",
        data={"username": "tester", "password": "password123", "remember_me": "false"},
        headers={"Accept": "application/json"},
    )
    assert login_response.status_code == 200

    response = client.get("/api/releases")
    assert response.status_code == 200
    assert response.get_json()["demo"]["title"] == "example"


def test_api_access_with_api_key(client, monkeypatch):
    monkeypatch.setattr(
        "app.services.services.TolokaService.get_titles_with_torrent_status",
        lambda: {"demo": {"title": "example"}},
    )

    response = client.get("/api/releases", headers={"X-API-Key": "test-api-key"})
    assert response.status_code == 200
    assert response.get_json()["demo"]["title"] == "example"


def test_api_access_requires_admin_role_for_user_jwt(app, client, existing_user):
    from app.routes.users import list_users

    token = _get_access_token(client, "tester", "password123")
    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        response = list_users()

    status_code = response[1] if isinstance(response, tuple) else response.status_code
    assert status_code == 403


def test_api_access_allows_admin_role_for_jwt(app, client, admin_user):
    from app.routes.users import list_users

    token = _get_access_token(client, "admin", "adminpass123")
    with app.test_request_context(headers={"Authorization": f"Bearer {token}"}):
        response = list_users()

    status_code = response[1] if isinstance(response, tuple) else response.status_code
    assert status_code == 200
    payload = (
        response[0].get_json() if isinstance(response, tuple) else response.get_json()
    )
    assert any(user["username"] == "admin" for user in payload)


def test_api_access_allows_admin_for_api_key(app):
    from app.routes.users import list_users

    with app.test_request_context(headers={"X-API-Key": "test-api-key"}):
        response = list_users()

    status_code = response[1] if isinstance(response, tuple) else response.status_code
    assert status_code == 200


def test_api_auth_me_with_jwt(client, existing_user):
    token = _get_access_token(client, "tester", "password123")
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["username"] == "tester"
