"""
@todo: break into separate modules
@todo: push "future" branch to GitHub and open WIP PR
@todo: add notes to README.rst in `master, pointing out "future" work
@todo: Allow creating projects
@todo: Allow deleting projects
@todo: Allow creating build types
@todo: Allow deleting build types
@todo: Allow pausing build types
@todo: Allow triggering builds
@todo: Allow canceling builds
@todo: docstrings for classes
"""

import itertools
import os
import urllib
import webbrowser

import dateutil.parser
import requests
from six.moves.urllib.parse import quote

from . import exceptions


def parse_date_string(date_string):
    return dateutil.parser.parse(date_string)


class PageJoiner(object):
    def __init__(self, query_set):
        self.query_set = query_set
        self.num_items = 0

    @property
    def url(self):
        return self.query_set.url

    def __len__(self):
        return self.num_items

    def __iter__(self):
        data = self.query_set._data()
        while data.get('count') > 0:
            for x in self.query_set:
                yield x
                self.num_items += 1
            if 'nextHref' in data:
                self.query_set._data_dict = None
                data = self.query_set._data(href=data['nextHref'])
            else:
                break


class Manager(object):
    def __init__(self, teamcity, query_set_factory):
        self.teamcity = teamcity
        self.query_set_factory = query_set_factory

    def all(self):
        return self.query_set_factory(teamcity=self.teamcity)


class TeamCity(object):
    username = None
    password = None
    server = None
    port = None
    protocol = None
    session = None
    projects = None

    def __init__(self,
                 username=None, password=None,
                 protocol='http', server='127.0.0.1', port=80,
                 session=None):
        self.username = username
        self.password = password
        self.protocol = protocol
        self.server = server
        self.port = port
        self.session = session or requests.Session()
        self.session.auth = (username, password)
        self.session.headers['Accept'] = 'application/json'
        self.projects = Manager(
            teamcity=self,
            query_set_factory=ProjectQuerySet)
        self.build_types = Manager(
            teamcity=self,
            query_set_factory=BuildTypeQuerySet)
        self.builds = Manager(
            teamcity=self,
            query_set_factory=BuildQuerySet)
        self.users = Manager(
            teamcity=self,
            query_set_factory=UserQuerySet)
        self.agents = Manager(
            teamcity=self,
            query_set_factory=AgentQuerySet)
        self.agent_pools = Manager(
            teamcity=self,
            query_set_factory=AgentPoolQuerySet)

        if self.username and self.password:
            self.base_url = "%s://%s:%d/httpAuth" % (
                self.protocol, self.server, self.port)
            self.auth = (self.username, self.password)
        else:
            self.base_url = "%s://%s:%d/guestAuth" % (
                self.protocol, self.server, self.port)
            self.auth = None

    @classmethod
    def from_environ(cls):
        return TeamCity(
            username=os.environ.get('TEAMCITY_USER'),
            password=os.environ.get('TEAMCITY_PASSWORD'),
            server=os.environ.get('TEAMCITY_HOST'))


class Parameter(object):
    def __init__(self, ptype=None, value=None):
        self.ptype = ptype
        self.value = value

    def __repr__(self):
        return '<%s.%s: ptype=%r value=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.ptype,
            self.value)


class WebBrowsable(object):
    def open_web_browser(self):
        webbrowser.open(self.web_url)


class Locator(object):
    dims = []

    def __init__(self):
        self._preds = []

    def add_pred(self, dim, value):
        # @todo: Check for invalid dims
        self._preds.append((dim, value))

    def __str__(self):
        return ','.join(['%s:%s' % p for p in self._preds])


class QuerySet(object):
    base_url = None
    _entity_factory = None

    def __init__(self, teamcity):
        self.teamcity = teamcity
        self.base_url = self.teamcity.base_url + self.__class__.uri
        self._locator = Locator()
        self._data_dict = {}

    def _add_pred(self, name, value):
        return self._locator.add_pred(name, value)

    def _get_url(self, details=False, href=None):
        if href is not None:
            return 'http://' + self.teamcity.server + href

        url = self.base_url

        locator_str = str(self._locator)
        if locator_str:
            if details:
                url += locator_str
            else:
                url += '?locator=' + locator_str

        return url

    def _fetch(self, details=False, href=None):
        self.url = self._get_url(details=details, href=href)
        res = self.teamcity.session.get(self.url)

        try:
            res.raise_for_status()
        except requests.HTTPError as e:
            status_code = e.response.status_code
            if status_code == 401:
                raise UnauthorizedError(
                    status_code=status_code,
                    msg=str(e),
                    text=e.response.text)
            raise

        if res.headers.get('Content-Type') == 'application/json':
            data = res.json()
        else:
            data = res.text

        return data

    def _data(self, details=False, href=None):
        if not self._data_dict:
            self._data_dict = self._fetch(details=details, href=href)

        return self._data_dict

    @classmethod
    def _from_dict(cls, d, query_set):
        return cls._entity_factory.from_dict(d, query_set)

    def get(self, just_url=False,
            raise_multiple_objects_returned=False,
            **kwargs):
        self.filter(**kwargs)
        if raise_multiple_objects_returned and len(self) > 1:
            raise exceptions.MultipleObjectsReturned()
        self._data_dict = None
        if just_url:
            return self._get_url(details=True)
        else:
            return self.__class__._from_dict(
                self._data(details=True), self)

    def __len__(self):
        data = self._data()
        return data['count']

    def __next__(self):
        return next(self.__iter__())

    next = __next__

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self, index, index + 1))
        except TypeError:
            return list(itertools.islice(
                self, index.start, index.stop, index.step))


class User(object):
    def __init__(self, id,
                 username, name, email, href, last_login_string,
                 query_set, data_dict=None):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.href = href
        self.last_login_string = last_login_string
        self.query_set = query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r username=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.username,
            self.name)

    @property
    def last_login_date(self):
        return parse_date_string(self.last_login_string)

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            id=d.get('id'),
            username=d.get('username'),
            name=d.get('name'),
            email=d.get('email'),
            href=d.get('href'),
            last_login_string=d.get('lastLogin'),
            query_set=query_set,
            data_dict=d)


class UserQuerySet(QuerySet):
    uri = '/app/rest/users/'
    _entity_factory = User

    def filter(self, id=None, username=None):
        if id is not None:
            self._add_pred('id', id)
        if username is not None:
            self._add_pred('username', username)
        return self

    def __iter__(self):
        return (self.__class__._entity_factory.from_dict(d, self)
                for d in self._data()['user'])


class BuildType(object):
    def __init__(self, id, name, description, href, web_url,
                 project_id, project_name,
                 paused, template_flag,
                 build_type_query_set, data_dict=None):
        self.id = id
        self.name = name
        self.description = description
        self.href = href
        self.web_url = web_url
        self.project_id = project_id
        self.project_name = project_name
        self.paused = paused
        self.template_flag = template_flag
        self.build_type_query_set = build_type_query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r name=%r project_name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name,
            self.project_name)

    @classmethod
    def from_dict(cls, d, build_type_query_set=None):
        return BuildType(
            id=d.get('id'),
            name=d.get('name'),
            description=d.get('description'),
            href=d.get('href'),
            web_url=d.get('webUrl'),
            project_id=d.get('projectId'),
            project_name=d.get('projectName'),
            paused=d.get('paused'),
            template_flag=d.get('templateFlag'),
            build_type_query_set=build_type_query_set,
            data_dict=d)

    @property
    def project(self):
        teamcity = self.build_type_query_set.teamcity
        return ProjectQuerySet(teamcity).get(id=self.project_id)

    @property
    def parameters_dict(self):
        d = {}

        for param in self._data_dict['parameters']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            if 'type' in param:
                param_obj.ptype = param['type']
            d[param['name']] = param_obj

        return d


class BuildTypeQuerySet(QuerySet):
    uri = '/app/rest/buildTypes/'
    _entity_factory = BuildType

    def filter(self, id=None, name=None,
               project_id=None, affected_project_id=None,
               paused=None, template_id=None, template_flag=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        if project_id is not None:
            self._add_pred('project', '(id:%s)' % project_id)
        if affected_project_id is not None:
            self._add_pred('affectedProject',
                           '(id:%s)' % affected_project_id)
        if paused is not None:
            self._add_pred('paused', paused)
        if template_id is not None:
            self._add_pred('template', '(id:%s)' % template_id)
        if template_flag is not None:
            self._add_pred('templateFlag', template_flag)
        return self

    def __iter__(self):
        return (BuildType.from_dict(d, self)
                for d in self._data()['buildType'])


class Project(WebBrowsable):
    def __init__(self, id, name, description,
                 href, web_url, parent_project_id,
                 project_query_set,
                 data_dict=None):
        self.id = id
        self.name = name
        self.description = description
        self.href = href
        self.web_url = web_url
        self.parent_project_id = parent_project_id
        self.project_query_set = project_query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name)

    @classmethod
    def from_dict(cls, d, project_query_set=None):
        return Project(
            id=d.get('id'),
            name=d.get('name'),
            description=d.get('description'),
            href=d.get('href'),
            web_url=d.get('webUrl'),
            parent_project_id=d.get('parentProjectId'),
            project_query_set=project_query_set,
            data_dict=d)

    @property
    def build_types(self):
        teamcity = self.project_query_set.teamcity
        return BuildTypeQuerySet(teamcity).filter(project_id=self.id)

    @property
    def projects(self):
        teamcity = self.project_query_set.teamcity
        project_query_set = ProjectQuerySet(teamcity)
        project_query_set._data_dict = self._data_dict['projects']
        return project_query_set

    @property
    def parent_project(self):
        teamcity = self.project_query_set.teamcity
        return ProjectQuerySet(teamcity).get(id=self.parent_project_id)

    @property
    def parameters_dict(self):
        d = {}

        for param in self._data_dict['parameters']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            if 'type' in param:
                param_obj.ptype = param['type']
            d[param['name']] = param_obj

        return d


class ProjectQuerySet(QuerySet):
    uri = '/app/rest/projects/'
    _entity_factory = Project

    def filter(self, id=None, name=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        return self

    def __iter__(self):
        return (Project.from_dict(d, self) for d in self._data()['project'])


class Agent(object):
    """
    (Pdb++) agent._data_dict.keys()
    [u'typeId', u'name', u'ip', u'enabled', u'properties',
     u'uptodate', u'href', u'connected', u'authorized',
     u'id', u'pool']
    """

    def __init__(self, id, href, name, type_id, ip,
                 enabled, connected, authorized,
                 pool_id,
                 query_set, data_dict=None):
        self.id = id
        self.href = href
        self.name = name
        self.type_id = type_id
        self.ip = ip
        self.enabled = enabled
        self.connected = connected
        self.authorized = authorized
        self.pool_id = pool_id
        self.query_set = query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name)

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            id=d.get('id'),
            href=d.get('href'),
            name=d.get('name'),
            type_id=d.get('typeId'),
            ip=d.get('ip'),
            enabled=d.get('enabled'),
            connected=d.get('connected'),
            authorized=d.get('authorized'),
            pool_id=d.get('pool', {}).get('id'),
            query_set=query_set,
            data_dict=d)

    @property
    def pool(self):
        teamcity = self.query_set.teamcity
        if 'agentPool' in self._data_dict:
            agent_pool = AgentPool.from_dict(self._data_dict.get('pool'))
        else:
            agent_pool = AgentPoolQuerySet(teamcity).get(id=self.pool_id)
        return agent_pool

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
    def teamcity(self):
        return self.query_set.teamcity

    def set_enabled(self, enabled_str, dry_run=False):
        extra_headers = {'Content-Type': 'text/plain',
                         'Accept': 'text/plain'}
        req = self._put_request('enabled', data=enabled_str,
                                extra_headers=extra_headers)
        if dry_run:
            return req
        return self.teamcity.session.send(req)

    def _put_request(self, relative_uri, data, extra_headers):
        url = self._get_url() + '/' + relative_uri
        headers = dict(self.teamcity.session.headers)
        headers.update(extra_headers)
        req= requests.Request(
            method='PUT',
            url=url,
            data=data,
            headers=headers)
        prepped = self.teamcity.session.prepare_request(req)
        return prepped

    def _get_url(self):
        return AgentQuerySet(self.teamcity).get(id=self.id, just_url=True)

    def enable(self, dry_run=False):
        return self.set_enabled('true', dry_run=dry_run)

    def disable(self, dry_run=False):
        return self.set_enabled('false', dry_run=dry_run)


class AgentQuerySet(QuerySet):
    uri = '/app/rest/agents/'
    _entity_factory = Agent

    def filter(self, id=None, name=None,
               connected=None, authorized=None, enabled=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        if connected is not None:
            self._add_pred('connected', connected)
        if authorized is not None:
            self._add_pred('authorized', authorized)
        if enabled is not None:
            self._add_pred('enabled', enabled)
        return self

    def __iter__(self):
        return (self._entity_factory.from_dict(d, self)
                for d in self._data()['agent'])


class AgentPool(object):
    def __init__(self, id, href, name,
                 query_set, data_dict=None):
        self.id = id
        self.href = href
        self.name = name
        self.query_set = query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name)

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            id=d.get('id'),
            href=d.get('href'),
            name=d.get('name'),
            query_set=query_set,
            data_dict=d)

    @property
    def agents(self):
        teamcity = self.query_set.teamcity
        ret = []
        for agent in self._data_dict['agents']['agent']:
            ret.append(Agent.from_dict(agent))
        return ret

    @property
    def projects(self):
        teamcity = self.query_set.teamcity
        ret = []
        for project in self._data_dict['projects']['project']:
            ret.append(Project.from_dict(project))
        return ret


class AgentPoolQuerySet(QuerySet):
    uri = '/app/rest/agentPools/'
    _entity_factory = AgentPool

    def filter(self, id=None, name=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        return self

    def __iter__(self):
        return (self._entity_factory.from_dict(d, self)
                for d in self._data()['agentPool'])


class Build(object):
    def __init__(self, id, number,
                 build_type_id,
                 queued_date_string, start_date_string, finish_date_string,
                 state, status, branch_name, href,
                 build_query_set, data_dict=None):
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
        if 'buildType' in self._data_dict:
            build_type = BuildType.from_dict(self._data_dict.get('buildType'))
        elif 'buildTypeId' in self._data_dict:
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
    def from_dict(cls, d, build_query_set):
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
        if not '+' in since_date:
            since_date += '+0000'

        since_date = quote(since_date)
        return since_date

    def __iter__(self):
        return (Build.from_dict(d, self)
                for d in self._data()['build'])
