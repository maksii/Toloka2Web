"""Anime model for storing anime metadata."""
from .base import db

class Anime(db.Model):
    """Model for storing anime information.
    
    Attributes:
        id: The primary key
        title: Anime title
        mailid: Associated mail ID
        tmdbdb: The Movie Database ID
    """
    __tablename__ = 'anime'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True, index=True)
    mailid = db.Column(db.String(100), nullable=True)
    tmdbdb = db.Column(db.String(100), nullable=True)
    
    def __repr__(self) -> str:
        """String representation of the Anime model."""
        return f'<Anime {self.title}>'
