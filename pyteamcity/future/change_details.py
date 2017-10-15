from . import exceptions
from .core.utils import raise_on_status


class ChangeDetails(object):
    def __init__(self, change):
        self.change = change
        teamcity = self.change.change_query_set.teamcity
        url = self.change.api_url
        res = teamcity.session.get(url)
        if res.status_code == 404:
            raise exceptions.ChangeDetailsNotFound(id=self.change.id)
        raise_on_status(res)
        self._data = res.json()
        self._metadata_url = url

    @property
    def comment(self):
        return self._data['comment']

    def __repr__(self):
        return '<%s.%s: change.id=%r comment=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.change.id,
            self.comment)