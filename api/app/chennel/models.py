from app import db


class Channel(db.Model):
    """Class for youtube channel table"""

    __tablename__ = 'channel'
    __table_args__ = (
        db.Index(
            'channel_youtube_id',  # Index name
            'youtube_id',
            unique=True
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    youtube_id = db.Column(db.String(20))

