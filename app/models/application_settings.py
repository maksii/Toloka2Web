"""Application settings model for storing global configuration."""
from .base import db

class ApplicationSettings(db.Model):
    """Model for storing application-wide settings.
    
    Attributes:
        id: The primary key
        section: Settings section/category name
        key: Setting key name
        value: Setting value
    """
    __tablename__ = 'application_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    
    __table_args__ = (
        db.UniqueConstraint('section', 'key', name='_app_setting_uc'),
    )