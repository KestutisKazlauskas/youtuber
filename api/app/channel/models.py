from app import db


class Channel(db.Model):
    """Class for youtube channel table"""

    __tablename__ = 'channel'

    id = db.Column(db.String(50), primary_key=True)  # youtube_id
    name = db.Column(db.String(100))

    # all channel videos first hour views medians
    views_median = db.Column(db.Integer)

