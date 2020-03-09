from datetime import timedelta,datetime
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import load_only
from sqlalchemy.sql import text
from statistics import median
import MySQLdb

from app import db
from app.common.helpers.common import is_string
from app.common.helpers.youtube_api import YouTubeApi
from app.channel.models import Channel
from app.video.models import Video, Statistic
from app.tags.models import Tag


class YoutubeChannelScrapeJob:
    """
    Cronjob for scraping videos and their statistics
    Scan time every 20 min because of youtube api limitation(*/20 * * * *) for channel with 2000
    videos
    """

    def __init__(self, app_config, range_=20):
        """Pass Flask app configs for cronjob"""
        self.app_config = app_config
        self.range = range_

    @staticmethod
    def _chunks(_list: list, n: int) -> list:
        """
        Split given list l to chunks of n items
        """
        for i in range(0, len(_list), n):
            yield _list[i : i + n]

    def _insert_tags(self, tags):
        """Method for inserting videos tags to database table"""
        for tag in tags:
            query = insert(Tag).prefix_with('IGNORE').values(
                name=tag
            )
            db.session.execute(query)
        db.session.commit()

    @staticmethod
    def _insert_videos(videos, channel_id):
        """Methods for inserting video to """
        for video in videos:
            query = insert(Video).prefix_with('IGNORE').values(
                id=video['youtube_id'],
                name=video['name'],
                published_at=video['published'],
                channel_id=channel_id
            )
            db.session.execute(query)
        db.session.commit()

    @staticmethod
    def _insert_statistics(videos):
        """Method for add video statistics records"""
        values = ','.join(
            '({0}, {1}, {2}, {3}, {4}, "{5}")'.format(
                video['views'],
                video['likes'],
                video['dislikes'],
                video['favorites'],
                video['comments'],
                video['youtube_id'],
            ) for video in videos
        )
        names = '(views, likes, dislikes, favorites, comments, video_id)'
        sql = 'INSERT INTO %s %s VALUES %s' % (Statistic.__tablename__, names, values)
        db.session.execute(text(sql))
        db.session.commit()

    @staticmethod
    def _count_first_hour_view(videos, range_):
        """Method for adding first_hour_views in video using liner interpolation"""
        for video in videos:
            now = datetime.now()
            hour = now - timedelta(hours=1)
            hour_range = now - timedelta(hours=1, minutes=range_)

            if hour > video['published'] > hour_range:
                # get statics and count and video
                statistic = Statistic.query.filter(
                    Statistic.video_id == video['youtube_id']
                ).order_by(Statistic.time_created.desc()).first()
                update = db.session.query(Video).filter(Video.id == video['youtube_id'])

                if statistic:
                    # liner interpolation method for getting first hour views
                    interval = (video['published'] + timedelta(hours=1)) - statistic.time_created
                    interval = int((interval.total_seconds() % 3600) // 60)

                    views = video['views'] - statistic.views
                    interpolated_views = statistic.views + int(round(views * interval/range_))
                    update.update({'first_hour_views': interpolated_views})

                else:
                    update.update({'first_hour_views': video['views']})
        db.session.commit()

    @staticmethod
    def _video_tag_relation(videos):
        """Method for relationship for videos tag"""
        for video in videos:
            if video.get('tags'):
                tags = Tag.query.options(load_only('id')).filter(Tag.name.in_(video['tags'])).all()

                tags_ids = ','.join('({0}, "{1}")'.format(tag.id, video['youtube_id']) for tag in tags)
                sql = 'INSERT IGNORE INTO tags (tag_id, video_id) VALUES %s' % tags_ids
                db.session.execute(text(sql))
        db.session.commit()

    @staticmethod
    def _count_channel_median(channel_id):
        """Method for counting median of all chanel videos first_hours_views"""
        videos = Video.query.options(load_only('first_hour_views'))\
            .filter(Video.first_hour_views != None).all()

        if videos:
            first_views = [video.first_hour_views for video in videos]

            db.session.query(Channel).filter(
                Channel.id == channel_id
            ).update({'views_median': median(first_views)})

    def run(self):
        """Method for running crontjob of youtube channel videos scraping"""
        channels = Channel.query.filter(Channel.views_median == None).all()
        for channel in channels:
            youtube = YouTubeApi(self.app_config['YOUTUBE_API_KEY'])

            while youtube.next_channel_page:
                video_ids = youtube.find_channel_videos(
                    channel.id,
                    page_token=is_string(youtube.next_channel_page)
                )
                if video_ids:
                    videos = youtube.get_videos_stats(video_ids)
                    self._insert_videos(videos, channel.id)

            # Update to not scrape channel again if it is scraped
            db.session.query(Channel).filter(
                Channel.id == channel.id
            ).update({'views_median': 1})
            db.session.commit()
