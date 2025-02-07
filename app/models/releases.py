"""Releases model for tracking media releases."""
from .base import db
from datetime import datetime

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
    """
    __tablename__ = 'releases'
    
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(100), nullable=False, unique=True, index=True)
    episode_index = db.Column(db.Integer)
    season_number = db.Column(db.String(10))
    torrent_name = db.Column(db.String(100))
    download_dir = db.Column(db.String(200))
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    release_group = db.Column(db.String(100))
    meta = db.Column(db.String(200))
    hash = db.Column(db.String(40))
    adjusted_episode_number = db.Column(db.Integer)
    guid = db.Column(db.String(50), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    
    def __repr__(self) -> str:
        """String representation of the Release model."""
        return f'<Release {self.section}>'