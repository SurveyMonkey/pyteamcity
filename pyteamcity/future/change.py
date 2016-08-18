from .core.queryset import QuerySet
from .core.utils import parse_date_string


class Change(object):
    def __init__(self, id,
                 version, username, date_str,
                 href, web_url,
                 query_set, data_dict=None):
        self.id = id
        self.version = version
        self.username = username
        self.date_str = date_str
        self.href = href
        self.web_url = web_url
        self.query_set = query_set
        self._data_dict = data_dict

    @property
    def date(self):
        return parse_date_string(self.date_str)

    def __repr__(self):
        return '<%s.%s: id=%r version=%r username=%r date=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.version,
            self.username,
            self.date.isoformat(),
        )

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            id=d.get('id'),
            version=d.get('version'),
            username=d.get('username'),
            date_str=d.get('date'),
            href=d.get('href'),
            web_url=d.get('webUrl'),
            query_set=query_set,
            data_dict=d)


class ChangeQuerySet(QuerySet):
    uri = '/app/rest/changes/'
    _entity_factory = Change

    def filter(self,
               id=None,
               project=None, build_type=None, build=None,
               vcs_root=None, username=None, version=None,
               start=None, count=None, lookup_limit=None):
        if id is not None:
            self._add_pred('id', id)
        if project is not None:
            self._add_pred('project', project)
        if build_type is not None:
            self._add_pred('buildType', build_type)
        if build is not None:
            self._add_pred('build', build)
        if vcs_root is not None:
            self._add_pred('vcsRoot', vcs_root)
        if username is not None:
            self._add_pred('username', username)
        if version is not None:
            self._add_pred('version', version)
        if start is not None:
            self._add_pred('start', start)
        if count is not None:
            self._add_pred('count', count)
        if lookup_limit is not None:
            self._add_pred('lookupLimit', lookup_limit)
        return self

    def __iter__(self):
        return (self.__class__._entity_factory.from_dict(d, self)
                for d in self._data()['change'])
