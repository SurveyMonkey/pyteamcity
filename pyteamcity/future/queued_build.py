from .core.parameter import Parameter
from .core.queryset import QuerySet
from .core.utils import parse_date_string
from .core.web_browsable import WebBrowsable

from .build_type import BuildType, BuildTypeQuerySet
from .user import User


class QueuedBuild(WebBrowsable):
    def __init__(self, id,
                 build_type_id,
                 queued_date_string,
                 branch_name, href, web_url,
                 build_query_set, data_dict=None):
        self.id = id
        self.build_type_id = build_type_id
        self.queued_date_string = queued_date_string
        self.branch_name = branch_name
        self.href = href
        self.web_url = web_url
        self.build_query_set = build_query_set
        self._data_dict = data_dict

    @property
    def user(self):
        if 'user' in self._data_dict.get('triggered', {}):
            return User.from_dict(self._data_dict['triggered']['user'])

    @property
    def queued_date(self):
        return parse_date_string(self.queued_date_string)

    @property
    def build_type(self):
        teamcity = self.build_query_set.teamcity
        if 'buildType' in self._data_dict:
            build_type = BuildType.from_dict(self._data_dict.get('buildType'))
        elif 'buildTypeId' in self._data_dict:
            build_type_id = self._data_dict['buildTypeId']
            build_type = BuildTypeQuerySet(teamcity).get(id=build_type_id)

        return build_type

    def __repr__(self):
        return '<%s.%s: id=%r build_type_id=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.build_type_id)

    @classmethod
    def from_dict(cls, d, build_query_set):
        return cls(
            id=d.get('id'),
            build_type_id=d.get('buildTypeId'),
            queued_date_string=d.get('queuedDate'),
            branch_name=d.get('branchName'),
            href=d.get('href'),
            web_url=d.get('webUrl'),
            build_query_set=build_query_set,
            data_dict=d)

    @property
    def parameters_dict(self):
        d = {}

        for param in self._data_dict['properties']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            if 'type' in param:
                param_obj.ptype = param['type']
            d[param['name']] = param_obj

        return d


class QueuedBuildQuerySet(QuerySet):
    uri = '/app/rest/buildQueue/'
    _entity_factory = QueuedBuild

    def filter(self,
               id=None,
               project=None,
               build_type=None, branch=None, user=None,
               start=None, count=None, lookup_limit=None):
        if id is not None:
            self._add_pred('id', id)
        if project is not None:
            self._add_pred('project', '(%s)' % project)
        if build_type is not None:
            self._add_pred('buildType', build_type)
        if branch is not None:
            self._add_pred('branch', branch)
        if user is not None:
            self._add_pred('user', '(%s)' % user)
        if start is not None:
            self._add_pred('start', start)
        if count is not None:
            self._add_pred('count', count)
        if lookup_limit is not None:
            self._add_pred('lookupLimit', lookup_limit)
        return self

    def __iter__(self):
        return (self._entity_factory.from_dict(d, self)
                for d in self._data().get('build', []))
