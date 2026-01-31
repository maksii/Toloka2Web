"""User settings model for storing user-specific configuration."""

from .base import db


class UserSettings(db.Model):
    """Model for storing user-specific settings.

    Attributes:
        id: The primary key
        user_id: Foreign key to the users table
        key: Setting key name
        value: Setting value
    """

    __tablename__ = "user_settings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(200), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "key", name="_user_setting_uc"),)
