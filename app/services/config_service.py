from typing import Dict, List
import configparser
import datetime

from app.models.application_settings import ApplicationSettings
from app.models.releases import Releases
from app.models.base import db
from app.services.base_service import BaseService


class ConfigService(BaseService):
    """Service for managing application configuration and releases."""

    @classmethod
    def read_all_settings_from_db(cls) -> List[Dict]:
        """Read all application settings from database."""
        settings = ApplicationSettings.query.all()
        return cls.serialize(settings)

    @classmethod
    def get_release_defaults(cls) -> Dict:
        """Get default values for the Add Release form (e.g. default_meta from Toloka section in DB)."""
        setting = ApplicationSettings.query.filter_by(
            section="Toloka", key="default_meta"
        ).first()
        default_meta = setting.value if setting else ""
        return {"default_meta": default_meta}

    @classmethod
    def init_web_settings(cls) -> None:
        """Initialize default web settings."""
        cls.add_new_setting("toloka2web", "open_registration", "True")
        cls.add_new_setting("toloka2web", "mal_api", "")
        cls.add_new_setting("toloka2web", "tmdb_api", "")

    @classmethod
    def add_new_setting(cls, section: str, key: str, value: str) -> None:
        """Add a new setting to the database."""
        new_setting = ApplicationSettings(section=section, key=key, value=value)
        db.session.add(new_setting)
        db.session.commit()
        cls.sync_settings("app", "to")

    @classmethod
    def update_setting(cls, id: int, section: str, key: str, value: str) -> None:
        """Update an existing setting in the database."""
        setting = ApplicationSettings.query.filter_by(id=id).first()
        if setting:
            setting.section = section
            setting.key = key
            setting.value = value
            db.session.add(setting)
            db.session.commit()
            cls.sync_settings("app", "to")

    @classmethod
    def delete_setting(cls, id: int) -> tuple[bool, str]:
        """Delete a setting from the database."""
        setting = ApplicationSettings.query.filter_by(id=id).first()
        if setting:
            db.session.delete(setting)
            db.session.commit()
            cls.sync_settings("app", "to")
            return True, "Setting deleted successfully."
        return False, "Setting not found."

    @classmethod
    def delete_release(cls, form: Dict) -> tuple[bool, str]:
        """Delete a release from the database."""
        section = form["codename"]
        release = Releases.query.filter_by(section=section).first()
        if release:
            db.session.delete(release)
            db.session.commit()
            cls.sync_settings("release", "to")
            return True, "Release deleted successfully."
        return False, "Release not found."

    @classmethod
    def edit_release(cls, form: Dict) -> None:
        """Edit or create a release in the database."""
        section = form["codename"]
        release = Releases.query.filter_by(section=section).first()
        if not release:
            release = Releases(section=section)
            db.session.add(release)

        # Update release attributes
        release.episode_index = int(form["episode_index"])
        release.season_number = form["season_number"]
        release.torrent_name = form["torrent_name"]
        release.download_dir = form["download_dir"]
        release.publish_date = datetime.datetime.strptime(
            form["publish_date"], "%y-%m-%d %H:%M"
        )
        release.release_group = form["release_group"]
        release.meta = form["meta"]
        release.hash = form["hash"]
        release.adjusted_episode_number = int(form["adjusted_episode_number"])
        release.guid = form["guid"]

        # Handle ongoing field - convert string to boolean
        ongoing_value = form.get("ongoing", "true")
        release.ongoing = ongoing_value in ("true", "True", True, "1", 1)

        db.session.commit()
        cls.sync_settings("release", "to")

    @classmethod
    def sync_settings(cls, setting_type: str, direction: str) -> None:
        """Synchronize settings between database and INI files."""
        paths = {"app": "data/app.ini", "release": "data/titles.ini"}

        actions = {
            ("app", "to"): cls.load_settings_from_db_and_write_to_ini,
            ("app", "from"): cls.read_settings_ini_and_sync_to_db,
            ("release", "to"): cls.load_releases_from_db_and_write_to_ini,
            ("release", "from"): cls.read_releases_ini_and_sync_to_db,
        }

        action = actions.get((setting_type, direction))
        if action:
            action(paths[setting_type])

    @classmethod
    def load_settings_from_db_and_write_to_ini(cls, file_path: str) -> None:
        """Write database settings to INI file."""
        settings = ApplicationSettings.query.all()
        config = configparser.ConfigParser()

        for setting in settings:
            if setting.section not in config.sections():
                config.add_section(setting.section)
            config.set(setting.section, setting.key, setting.value)

        with open(file_path, "w", encoding="utf-8") as configfile:
            config.write(configfile)

    @classmethod
    def read_settings_ini_and_sync_to_db(cls, file_path: str) -> None:
        """Read settings from INI file and sync to database."""
        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf-8")

        for section in config.sections():
            for key, value in config.items(section):
                setting = ApplicationSettings.query.filter_by(
                    section=section, key=key
                ).first()
                if setting:
                    setting.value = value
                else:
                    new_setting = ApplicationSettings(
                        section=section, key=key, value=value
                    )
                    db.session.add(new_setting)
        db.session.commit()

    @classmethod
    def load_releases_from_db_and_write_to_ini(cls, file_path: str) -> None:
        """Write database releases to INI file."""
        releases = Releases.query.all()
        config = configparser.ConfigParser()

        for release in releases:
            section = release.section
            if section not in config.sections():
                config.add_section(section)
            config.set(section, "episode_index", str(release.episode_index))
            config.set(section, "season_number", release.season_number)
            config.set(section, "torrent_name", release.torrent_name)
            config.set(section, "download_dir", release.download_dir)
            config.set(
                section, "publish_date", release.publish_date.strftime("%y-%m-%d %H:%M")
            )
            config.set(section, "release_group", release.release_group)
            config.set(section, "meta", release.meta)
            config.set(section, "hash", release.hash)
            config.set(
                section, "adjusted_episode_number", str(release.adjusted_episode_number)
            )
            config.set(section, "guid", release.guid)
            config.set(
                section,
                "is_partial_season",
                str(release.ongoing if release.ongoing is not None else True),
            )

        with open(file_path, "w", encoding="utf-8") as configfile:
            config.write(configfile)

    @classmethod
    def read_releases_ini_and_sync_to_db(cls, file_path: str) -> None:
        """Read releases from INI file and sync to database."""
        config = configparser.ConfigParser()
        config.read(file_path, encoding="utf-8")

        for section in config.sections():
            release = Releases.query.filter_by(section=section).first()
            if not release:
                release = Releases(section=section)
                db.session.add(release)

            release.episode_index = int(
                config.get(section, "episode_index", fallback="1")
            )
            release.season_number = config.get(section, "season_number", fallback="1")
            release.torrent_name = config.get(section, "torrent_name", fallback="")
            release.download_dir = config.get(section, "download_dir", fallback="")

            try:
                release.publish_date = datetime.datetime.strptime(
                    config.get(section, "publish_date"), "%y-%m-%d %H:%M"
                )
            except (configparser.NoOptionError, ValueError):
                release.publish_date = datetime.datetime.now()

            release.release_group = config.get(section, "release_group", fallback="")
            release.meta = config.get(section, "meta", fallback="")
            release.hash = config.get(section, "hash", fallback="")
            release.adjusted_episode_number = int(
                config.get(section, "adjusted_episode_number", fallback="1")
            )
            release.guid = config.get(section, "guid", fallback="")

            # Handle is_partial_season from INI (displayed as "Ongoing" in UI) - default to True for backward compatibility
            is_partial_str = config.get(section, "is_partial_season", fallback="True")
            release.ongoing = is_partial_str.lower() in ("true", "1", "yes")

        db.session.commit()
