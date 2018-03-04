from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import load_only
from sqlalchemy.sql import text

from app import db
from app.common.helpers.common import is_string
from app.common.helpers.youtube_api import YouTubeApi
from app.video.models import Video
from app.tags.models import Tag


class YoutubeChannelScrapeJob:

    def __init__(self, app_config):
        """Pass Flask app configs for cronjob"""
        self.app_config = app_config

    # def _db_settings(self):

    @staticmethod
    def _insert_tags(tags):
        """Method for inserting videos tags to database table"""
        tags_values = ','.join('("{0}")'.format(tag) for tag in tags)
        sql = 'INSERT IGNORE INTO %s (name) VALUES %s' % (Tag.__tablename__, tags_values)

        db.session.execute(text(sql))
        db.session.commit()

    @staticmethod
    def _insert_videos(videos):
        """Methods for inserting video to """
        for video in videos:
            tags = Tag.query.options(load_only('id')).filter(Tag.name.in_(video['tags'])).all()
            query = insert(Video).values(
                name=video['name'],
                youtube_id=video['youtube_id'],
                published_at=video['published'],
                views=video['views'],
            ).on_duplicate_key_update(
                views=video['views']
            )
            db.session.execute(query)
        db.session.commit()

    @staticmethod
    def _video_tag_relation(videos):
        """Method for relationship for videos tag"""
        for video in videos:
            tags = Tag.query.options(load_only('id')).filter(Tag.name.in_(video['tags'])).all()
            video = Video.query.options(
                load_only('id')).filter(Video.youtube_id == video['youtube_id']
            ).one()

            tags_ids = ','.join('({0}, {1})'.format(tag.id, video.id) for tag in tags)
            sql = 'INSERT IGNORE INTO tags (tag_id, video_id) VALUES %s' % tags_ids
            db.session.execute(text(sql))
        db.session.commit()

    def run(self):
        """Method for running crontjob of youtube channel videos scraping"""
        youtube = YouTubeApi(self.app_config['YOUTUBE_API_KEY'])

        while youtube.next_channel_page:
            # TODO add channel to database.
            video_ids = youtube.find_channel_videos(
                'UCMfPBtm9CWGswAXohT5MFyQ',
                page_token=is_string(youtube.next_channel_page) # check if token is not boolean
            )
            videos = youtube.get_videos_stats(video_ids)

            tags = []
            for video in videos:
                tags.extend(video['tags'])

            self._insert_tags(list(set(tags)))
            self._insert_videos(videos)
            self._video_tag_relation(videos)
