from app import db
from app.channel.models import Channel
from sqlalchemy.sql import func
from app.common.helpers.common import datetime_to_string

association_table = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('video_id', db.String(20), db.ForeignKey('video.id'), primary_key=True)
)


class Video(db.Model):
    """Class for youtube video statistics table"""

    __tablename__ = 'video'

    id = db.Column(db.String(20), primary_key=True)  # youtube_id
    name = db.Column(db.String(100))
    published_at = db.Column(db.DateTime())

    # calculate after an hour after creation for performance
    first_hour_views = db.Column(db.Integer())

    tags = db.relationship(
        'Tag', secondary=association_table, lazy='subquery',
        backref=db.backref('videos', lazy=True)
    )
    channel_id = db.Column(db.String(20), db.ForeignKey('channel.id'))
    channel = db.relationship(Channel)
    statistics = db.relationship('Statistic', lazy='noload')  # do not load with videos

    # TimeStamps
    time_created = db.Column(db.DateTime(), server_default=func.now())
    time_updated = db.Column(db.DateTime(), onupdate=func.now())

    @property
    def serialize(self):
        """Method for makings json serializable object"""
        return {
            'id': self.id,
            'name': self.name,
            'published_at': datetime_to_string(self.published_at),
            'tags': self.tags_serialize
        }

    @property
    def tags_serialize(self):
        """Method for serializing many to many relationship"""
        return [item.serialize for item in self.tags if self.tags]


class Statistic(db.Model):
    """Class for saving video statistics"""

    __tablename__ = 'statistic'

    id = db.Column(db.BigInteger, primary_key=True)
    views = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)
    favorites = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    video_id = db.Column(db.String(20), db.ForeignKey('video.id'))

    # Timestamp
    time_created = db.Column(db.DateTime(), server_default=func.now())