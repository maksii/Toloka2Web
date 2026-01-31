import sys
import types
from pathlib import Path

import pytest


def _stub_module(module_name, attributes, is_package=False):
    module = types.ModuleType(module_name)
    if is_package:
        module.__path__ = []
    for key, value in attributes.items():
        setattr(module, key, value)
    sys.modules[module_name] = module
    return module


def _ensure_optional_dependencies():
    try:
        import toloka2MediaServer  # noqa: F401
    except ImportError:
        _stub_module("toloka2MediaServer", {}, is_package=True)

        def load_configurations(app_path, titles_path):
            application_config = types.SimpleNamespace(client="qbit", default_download_dir="")
            return {}, {}, application_config

        def get_toloka_client(application_config):
            return object()

        _stub_module(
            "toloka2MediaServer.config_parser",
            {
                "load_configurations": load_configurations,
                "get_toloka_client": get_toloka_client,
            },
        )

        def dynamic_client_init(config):
            return types.SimpleNamespace(
                get_torrent_info=lambda **kwargs: types.SimpleNamespace(data=[])
            )

        _stub_module("toloka2MediaServer.clients", {}, is_package=True)
        _stub_module("toloka2MediaServer.clients.dynamic", {"dynamic_client_init": dynamic_client_init})

        class Config:
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)

        _stub_module("toloka2MediaServer.models", {}, is_package=True)
        _stub_module("toloka2MediaServer.models.config", {"Config": Config})

        def setup_logging(path):
            return types.SimpleNamespace(info=lambda *args, **kwargs: None)

        _stub_module("toloka2MediaServer.logger_setup", {"setup_logging": setup_logging})

        class OperationResult:
            def __init__(self):
                self.operation_type = types.SimpleNamespace(name="noop")
                self.torrent_references = []
                self.titles_references = []
                self.status_message = ""
                self.response_code = types.SimpleNamespace(name="noop")
                self.operation_logs = []
                self.start_time = None
                self.end_time = None

        def _operation_result():
            return OperationResult()

        _stub_module(
            "toloka2MediaServer.main_logic",
            {
                "add_release_by_url": lambda *_args, **_kwargs: _operation_result(),
                "update_release_by_name": lambda *_args, **_kwargs: _operation_result(),
                "update_releases": lambda *_args, **_kwargs: _operation_result(),
                "search_torrents": lambda *_args, **_kwargs: types.SimpleNamespace(response={}),
                "get_torrent": lambda *_args, **_kwargs: types.SimpleNamespace(response={}),
                "add_torrent": lambda *_args, **_kwargs: _operation_result(),
            },
        )

    try:
        import stream2mediaserver  # noqa: F401
    except ImportError:
        _stub_module("stream2mediaserver", {}, is_package=True)

        class MainLogic:
            def search_releases(self, query):
                return {}

            def get_release_details(self, provider_name, release_url):
                return {}

        _stub_module("stream2mediaserver.main_logic", {"MainLogic": MainLogic})


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_ensure_optional_dependencies()


@pytest.fixture()
def app(tmp_path, monkeypatch):
    from app.app import create_app
    from app.models.base import db
    from app.services.config_service import ConfigService
    from app.services.services_db import DatabaseService

    monkeypatch.setattr(ConfigService, "sync_settings", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        ConfigService, "read_settings_ini_and_sync_to_db", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        ConfigService, "read_releases_ini_and_sync_to_db", lambda *args, **kwargs: None
    )
    monkeypatch.setattr(DatabaseService, "initialize_database", lambda *args, **kwargs: None)

    database_path = tmp_path / "toloka2web_test.db"
    app = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test-secret",
            "JWT_SECRET_KEY": "jwt-secret",
            "API_KEY": "test-api-key",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "WTF_CSRF_ENABLED": False,
            "CORS_ORIGINS": ["*"],
        }
    )

    with app.app_context():
        yield app
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
