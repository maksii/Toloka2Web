from .base import db
from datetime import datetime

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True)
    mailid = db.Column(db.String(100), nullable=True)
    tmdbdb = db.Column(db.String(100), nullable=True)
