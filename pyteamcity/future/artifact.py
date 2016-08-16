import fnmatch
import os

from . import exceptions
from .core.utils import parse_date_string


class Artifact(object):
    def __init__(self, build, path=''):
        self.build = build
        self.path = path
        teamcity = self.build.build_query_set.teamcity
        url = self.build.api_url + '/artifacts/metadata/' + self.path
        res = teamcity.session.get(url)
        if not res.ok:
            if res.status_code == 404:
                raise exceptions.ArtifactNotFound(path=path)
            else:
                raise exceptions.HTTPError(
                    status_code=res.status_code,
                    reason=res.reason,
                    text=res.text)
        self._data = res.json()
        self._metadata_url = url

    @property
    def name(self):
        return self._data['name']

    def getsize(self):
        return self._data.get('size')

    @property
    def size(self):
        return self.getsize()

    @property
    def modification_time(self):
        return parse_date_string(self._data['modificationTime'])

    def splitext(self):
        return os.path.splitext(self.name)

    @property
    def ext(self):
        return self.splitext()[1]

    def fnmatch(self, pattern):
        return fnmatch.fnmatch(self.name, pattern)

    @property
    def content_href(self):
        return self._data.get('content', {}).get('href')

    def isdir(self):
        return self.content_href is None

    def isfile(self):
        return self.content_href is not None

    def __repr__(self):
        return '<%s.%s: build.id=%r name=%r size=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.build.id,
            self.name,
            self.size)

    def content(self):
        if not self.isfile():
            raise exceptions.IllegalOperation(
                'Calling the `content` method on a non-file artifact'
                ' (%r) is not allowed' % self)
        teamcity = self.build.build_query_set.teamcity
        url = teamcity.base_base_url + self.content_href
        res = teamcity.session.get(url)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        return res.content

    def get_artifact_by_path(self, path):
        return Artifact(build=self.build,
                        path=os.path.join(self.path, path))

    def __div__(self, path):
        return self.get_artifact_by_path(path)

    # Python 3
    __truediv__ = __div__

    def listdir(self, pattern=None):
        teamcity = self.build.build_query_set.teamcity
        url = self.build.api_url + '/artifacts/children/' + self.path
        res = teamcity.session.get(url)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        data = res.json()
        ret = []
        for f in data['file']:
            if pattern is None or fnmatch.fnmatch(f['name'], pattern):
                path = self.path + '/' + f['name']
                path = path.lstrip('/')
                ret.append(Artifact(build=self.build, path=path))
        return ret

    def dirname(self):
        path = os.path.dirname(self.path)
        return Artifact(build=self.build, path=path)

    def files(self, pattern=None):
        return [x for x in self.listdir(pattern) if x.isfile()]

    def dirs(self, pattern=None):
        return [x for x in self.listdir(pattern) if x.isdir()]
