from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Music(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150))
    artist = db.Column(db.String(150))
    category = db.Column(db.String(150))
    year = db.Column(db.Integer)
    album = db.Column(db.String(150))
    
    def __init__(self, title, artist, category, year, album):
        self.title = title
        self.artist = artist
        self.category = category
        self.year = year
        self.album = album