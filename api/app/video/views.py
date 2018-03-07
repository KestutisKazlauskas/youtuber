from flask import request
from flask_api import response
from sqlalchemy import text
from app import db

from app.common.helpers.api_view import MainMethodView
from app.common.helpers.common import to_float
from app.channel.models import Channel
from app.video.models import Video
from app.tags.models import Tag
from . import video_blueprint


class VideoView(MainMethodView):

    def get(self):
        """Method for getting and searching videos by tags and performance"""

        tags = self._get_list_params(request.args.get('tags'))
        performance = to_float(request.args.get('performance'))
        limit, offset = self._get_limit_offset(
            request.args.get('limit'), request.args.get('offset')
        )

        data = {}
        videos = []

        if tags:
            videos = Video.query.join(Video.tags).filter(Tag.id.in_(tags))

        # Todo make all request raw sql;
        if performance:
            sql = "select v.id from video v inner join channel ch on "
            sql += "v.channel_id = ch.id and v.first_hour_views is not NULL and "
            sql += "v.first_hour_views/ch.views_median >= %s limit %s offset %s" % (performance,
                                                                                  limit, offset)
            rows = db.session.execute(text(sql))
            videos = Video.query.filter(Video.id.in_([row['id'] for row in rows]))

        if not tags and not performance:
            videos = Video.query

        if videos:
            count = videos.count()
            videos = videos.order_by(Video.first_hour_views.desc()).limit(limit).offset(offset)
            data = {
                'items': [video.serialize for video in videos],
                'count': count
            }

        return response.APIResponse(data)


# register video view api and make urls
video_view = VideoView.as_view('video_view')
video_blueprint.add_url_rule('/api/videos', view_func=video_view, methods=['GET'])
