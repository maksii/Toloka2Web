from .base import db
from datetime import datetime

class Releases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    episode_index = db.Column(db.Integer)
    season_number = db.Column(db.String(10))
    ext_name = db.Column(db.String(10))
    torrent_name = db.Column(db.String(100))
    download_dir = db.Column(db.String(200))
    publish_date = db.Column(db.DateTime)
    release_group = db.Column(db.String(100))
    meta = db.Column(db.String(200))
    hash = db.Column(db.String(40))
    adjusted_episode_number = db.Column(db.Integer)
    guid = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)