from flask.views import MethodView

from app.common.helpers.common import to_int


class MainMethodView(MethodView):

    @staticmethod
    def _get_list_params(params_stirng):
        """Method for getting list of tags from request tag sting"""
        params = []
        if params_stirng:
            params = params_stirng.split(',')

        return params

    @staticmethod
    def _get_int(value, default):
        value = to_int(value)
        if not value:
            value = default

        return value

    def _get_limit_offset(self, limit, offset):
        """Method for setting limit offset for filtering records"""

        return self._get_int(limit, 50), self._get_int(offset, 0)