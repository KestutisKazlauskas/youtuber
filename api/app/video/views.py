from flask import request
from flask_api import response

from app.common.helpers.api_view import MainMethodView
from app.video.models import Video
from app.tags.models import Tag
from . import video_blueprint


class VideoView(MainMethodView):

    def get(self):
        """Method for getting and searching videos by tags and performance"""

        tags = self._get_list_params(request.args.get('tags'))
        limit, offset = self._get_limit_offset(
            request.args.get('limit'), request.args.get('offset')
        )

        data = {}
        videos = []
        if tags:
            videos = Video.query.join(Video.tags).filter(Tag.id.in_(tags))

        if not videos:
            videos = Video.query

        if videos:
            count = videos.count()
            videos.limit(limit).offset(offset).all()
            data = {
                'items': [video.serialize for video in videos],
                'count': count
            }

        return response.APIResponse(data)


# register video view api and make urls
video_view = VideoView.as_view('video_view')
video_blueprint.add_url_rule('/api/videos', view_func=video_view, methods=['GET'])
