from app import db
from app.chennel.models import Channel
from sqlalchemy.sql import func
from app.common.helpers.common import datetime_to_string

association_table = db.Table(
    'tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('video_id', db.Integer, db.ForeignKey('video.id'), primary_key=True)
)


class Video(db.Model):
    """Class for youtube video statistics table"""

    __tablename__ = 'video'
    __table_args__ = (
        db.Index(
            'video_youtube_id',  # Index name
            'youtube_id',
            unique=True
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    youtube_id = db.Column(db.String(20))

    # Statistics if need to track every changes
    # need to move to other table
    published_at = db.Column(db.DateTime())
    views_on_creation = db.Column(db.DateTime())
    views = db.Column(db.Integer())

    # calculate after an hour after creation for performance
    first_hour_views = db.Column(db.Integer())

    tags = db.relationship(
        'Tag', secondary=association_table, lazy='subquery',
        backref=db.backref('videos', lazy=True)
    )
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'))
    channel = db.relationship(Channel)

    # TimeStamps
    time_created = db.Column(db.DateTime(), server_default=func.now())
    time_updated = db.Column(db.DateTime(), onupdate=func.now())

    @property
    def serialize(self):
        """Method for makings json serializable object"""
        return {
            'id': self.id,
            'name': self.name,
            'youtube_id': self.youtube_id,
            'published_at': datetime_to_string(self.published_at),
            'tags': self.tags_serialize
        }

    @property
    def tags_serialize(self):
        """Method for serializing many to many relationship"""
        return [item.serialize for item in self.tags if self.tags]