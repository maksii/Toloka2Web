"""Releases model for tracking media releases."""
from datetime import datetime, timezone

from .base import db

class Releases(db.Model):
    """Model for tracking media releases.
    
    Attributes:
        id: The primary key
        section: Unique section identifier
        episode_index: Episode number
        season_number: Season number
        torrent_name: Name of the torrent file
        download_dir: Download directory path
        publish_date: Release publication date
        release_group: Name of the release group
        meta: Additional metadata
        hash: Torrent hash
        adjusted_episode_number: Corrected episode number
        guid: Global unique identifier
        user_id: Foreign key to users table
        ongoing: Whether this release is ongoing (auto-update enabled)
    """
    __tablename__ = 'releases'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False, unique=True, index=True)
    episode_index = db.Column(db.Integer)
    season_number = db.Column(db.String(10))
    torrent_name = db.Column(db.String(100))
    download_dir = db.Column(db.String(200))
    publish_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    release_group = db.Column(db.String(100))
    meta = db.Column(db.String(200))
    hash = db.Column(db.String(40))
    adjusted_episode_number = db.Column(db.Integer)
    guid = db.Column(db.String(50), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    ongoing = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self) -> str:
        """String representation of the Release model."""
        return f'<Release {self.section}>'