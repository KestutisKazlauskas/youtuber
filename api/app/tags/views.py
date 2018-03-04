from flask import request
from flask_api import response

from app.common.helpers.api_view import MainMethodView
from app.tags.models import Tag
from . import tag_blueprint


class TagView(MainMethodView):

    def get(self):
        """Method for filtering tags"""
        name = request.args.get('name')
        limit, offset = self._get_limit_offset(
            request.args.get('limit'), request.args.get('offset')
        )

        data = {}
        tags = []
        if name:
            tags = Tag.query.filter(Tag.name.like('%{0}%'.format(name)))

        if not tags:
            tags = Tag.query

        if tags:
            count = tags.count()
            tags.limit(limit).offset(offset).all()
            data = {
                'items': [tag.serialize for tag in tags],
                'count': count
            }

        return response.APIResponse(data)


# regester tag api url
tag_view = TagView.as_view('tag_view')
tag_blueprint.add_url_rule('/api/tags', view_func=tag_view, methods=['GET'])