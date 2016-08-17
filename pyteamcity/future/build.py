from six.moves.urllib.parse import quote

from . import exceptions
from .core.parameter import Parameter
from .core.queryset import QuerySet
from .core.utils import parse_date_string

from .agent import Agent
from .artifact import Artifact
from .build_type import BuildTypeQuerySet
from .user import User


class Build(object):
    def __init__(self, id, number,
                 build_type_id,
                 queued_date_string, start_date_string, finish_date_string,
                 state, status, branch_name, href,
                 build_query_set, teamcity, data_dict=None):
        self.id = id
        self.number = number
        self.queued_date_string = queued_date_string
        self.start_date_string = start_date_string
        self.finish_date_string = finish_date_string
        self.build_type_id = build_type_id
        self.state = state
        self.status = status
        self.branch_name = branch_name
        self.href = href
        self.build_query_set = build_query_set
        self.teamcity = teamcity
        if self.teamcity is None and self.build_query_set is not None:
            self.teamcity = self.build_query_set.teamcity
        self._data_dict = data_dict

    @property
    def user(self):
        if 'user' in self._data_dict.get('triggered', {}):
            return User.from_dict(self._data_dict['triggered']['user'])

    @property
    def queued_date(self):
        return parse_date_string(self.queued_date_string)

    @property
    def start_date(self):
        return parse_date_string(self.start_date_string)

    @property
    def finish_date(self):
        return parse_date_string(self.finish_date_string)

    @property
    def agent(self):
        return Agent.from_dict(self._data_dict.get('agent'))

    @property
    def build_type(self):
        teamcity = self.build_query_set.teamcity
        build_type_id = self._data_dict['buildTypeId']
        build_type = BuildTypeQuerySet(teamcity).get(id=build_type_id)

        return build_type

    def __repr__(self):
        return '<%s.%s: id=%r build_type_id=%r number=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.build_type_id,
            self.number)

    @classmethod
    def from_dict(cls, d, build_query_set=None, teamcity=None):
        return Build(
            id=d.get('id'),
            number=d.get('number'),
            queued_date_string=d.get('queuedDate'),
            start_date_string=d.get('startDate'),
            finish_date_string=d.get('finishDate'),
            build_type_id=d.get('buildTypeId'),
            state=d.get('state'),
            status=d.get('status'),
            branch_name=d.get('branchName'),
            href=d.get('href'),
            build_query_set=build_query_set,
            teamcity=teamcity,
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

    @property
    def api_url(self):
        teamcity = self.build_query_set.teamcity
        base_url = teamcity.base_url
        url = base_url + '/app/rest/builds/id:%s' % self.id
        return url

    @property
    def artifacts(self):
        return Artifact(build=self)

    def pin(self, comment):
        url = self.teamcity.base_base_url + self.href + '/pin'
        res = self.teamcity.session.put(url=url, data=comment)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        return self

    def unpin(self):
        url = self.teamcity.base_base_url + self.href + '/pin'
        res = self.teamcity.session.delete(url=url)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        return self


class BuildQuerySet(QuerySet):
    uri = '/app/rest/builds/'
    _entity_factory = Build

    def filter(self,
               id=None,
               project=None, affected_project=None,
               build_type=None, number=None, branch=None, user=None,
               tags=None, pinned=None,
               since_build=None, since_date=None, status=None,
               agent_name=None, personal=None,
               canceled=None, failed_to_start=None, running=None,
               start=None, count=None, lookup_limit=None):
        if id is not None:
            self._add_pred('id', id)
        if project is not None:
            self._add_pred('project', '(%s)' % project)
        if affected_project is not None:
            self._add_pred('affectedProject', '(%s)' % affected_project)
        if build_type is not None:
            self._add_pred('buildType', build_type)
        if number is not None:
            self._add_pred('number', number)
        if branch is not None:
            self._add_pred('branch', branch)
        if user is not None:
            self._add_pred('user', '(%s)' % user)
        if tags is not None:
            if not hasattr(tags, 'split'):
                tags = ','.join(tags)
            self._add_pred('tags', tags)
        if pinned is not None:
            self._add_pred('pinned', pinned)
        if since_build is not None:
            self._add_pred('sinceBuild', '(%s)' % since_build)
        if since_date is not None:
            since_date = self._get_since_date(since_date)
            self._add_pred('sinceDate', since_date)
        if status is not None:
            self._add_pred('status', status)
        if agent_name is not None:
            self._add_pred('agentName', agent_name)
        if personal is not None:
            self._add_pred('personal', personal)
        if canceled is not None:
            self._add_pred('canceled', canceled)
        if failed_to_start is not None:
            self._add_pred('failedToStart', failed_to_start)
        if running is not None:
            self._add_pred('running', running)
        if start is not None:
            self._add_pred('start', start)
        if count is not None:
            self._add_pred('count', count)
        if lookup_limit is not None:
            self._add_pred('lookupLimit', lookup_limit)
        return self

    def _get_since_date(self, since_date):
        if hasattr(since_date, 'strftime'):
            since_date = since_date.strftime('%Y%m%dT%H%M%S%z')

        # If there's no timezone, assume UTC
        if '+' not in since_date:
            since_date += '+0000'

        since_date = quote(since_date)
        return since_date

    def __iter__(self):
        return (Build.from_dict(d, self, teamcity=self.teamcity)
                for d in self._data()['build'])
