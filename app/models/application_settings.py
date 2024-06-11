from .base import db

class ApplicationSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section = db.Column(db.String(50), nullable=False)
    key = db.Column(db.String(50), nullable=False)
    value = db.Column(db.String(255), nullable=False)