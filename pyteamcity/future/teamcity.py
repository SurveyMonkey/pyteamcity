import os

import requests

from . import exceptions
from .core.manager import Manager
from .core.utils import parse_date_string

from .agent import AgentQuerySet
from .agent_pool import AgentPoolQuerySet
from .build import BuildQuerySet
from .build_type import BuildTypeQuerySet
from .change import ChangeQuerySet
from .project import ProjectQuerySet
from .queued_build import QueuedBuildQuerySet
from .user import UserQuerySet
from .user_group import UserGroupQuerySet
from .vcs_root import VCSRootQuerySet


class Plugin(object):
    def __init__(self, name, display_name, version, load_path):
        self.name = name
        self.display_name = display_name
        self.version = version
        self.load_path = load_path

    def __repr__(self):
        return '<%s.%s: name=%r display_name=%r version=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.name,
            self.display_name,
            self.version,
        )


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
                 protocol='http', server='127.0.0.1', port=None,
                 session=None):
        self.username = username
        self.password = password
        self.protocol = protocol
        self.server = server
        self.port = port or (443 if protocol == 'https' else 80)
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
        self.queued_builds = Manager(
            teamcity=self,
            query_set_factory=QueuedBuildQuerySet)
        self.users = Manager(
            teamcity=self,
            query_set_factory=UserQuerySet)
        self.user_groups = Manager(
            teamcity=self,
            query_set_factory=UserGroupQuerySet)
        self.agents = Manager(
            teamcity=self,
            query_set_factory=AgentQuerySet)
        self.agent_pools = Manager(
            teamcity=self,
            query_set_factory=AgentPoolQuerySet)
        self.vcs_roots = Manager(
            teamcity=self,
            query_set_factory=VCSRootQuerySet)
        self.changes = Manager(
            teamcity=self,
            query_set_factory=ChangeQuerySet)

        self.base_base_url = "%s://%s" % (
            self.protocol, self.server)
        if self.protocol == 'http' and self.port != 80:
            self.base_base_url += ':%d' % self.port
        if self.protocol == 'https' and self.port != 443:
            self.base_base_url += ':%d' % self.port

        if self.username and self.password:
            self.base_url = self.base_base_url + '/httpAuth'
            self.auth = (self.username, self.password)
        else:
            self.base_url = self.base_base_url + '/guestAuth'
            self.auth = None

    def relative_url(self, uri):
        return '%s/%s' % (self.base_url, uri)

    @classmethod
    def from_environ(cls):
        return TeamCity(
            protocol=os.environ.get('TEAMCITY_PROTO'),
            username=os.environ.get('TEAMCITY_USER'),
            password=os.environ.get('TEAMCITY_PASSWORD'),
            server=os.environ.get('TEAMCITY_HOST'))

    def plugins(self):
        url = self.base_url + '/app/rest/server/plugins'
        res = self.session.get(url)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        data = res.json()
        plugins = []
        for plugin in data['plugin']:
            plugins.append(
                Plugin(name=plugin.get('name'),
                       display_name=plugin.get('displayName'),
                       version=plugin.get('version'),
                       load_path=plugin.get('loadPath'))
            )
        return plugins

    @property
    def server_info(self):
        url = self.base_url + '/app/rest/server'
        res = self.session.get(url)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        data = res.json()
        return TeamCityServerInfo(
            version=data['version'],
            version_major=data['versionMajor'],
            version_minor=data['versionMinor'],
            build_number=data['buildNumber'],
            start_time_str=data['startTime'],
            current_time_str=data['currentTime'],
            build_date_str=data['buildDate'],
            internal_id=data['internalId'],
            web_url=data['webUrl'])


class TeamCityServerInfo(object):
    def __init__(self,
                 version, version_major, version_minor, build_number,
                 start_time_str, current_time_str, build_date_str,
                 internal_id, web_url):
        self.version = version
        self.version_major = version_major
        self.version_minor = version_minor
        self.build_number = build_number
        self.start_time_str = start_time_str
        self.current_time_str = current_time_str
        self.build_date_str = build_date_str
        self.internal_id = internal_id
        self.web_url = web_url

    def __repr__(self):
        return '<%s.%s: web_url=%r version=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.web_url,
            self.version)

    @property
    def start_time(self):
        return parse_date_string(self.start_time_str)

    @property
    def current_time(self):
        return parse_date_string(self.current_time_str)

    @property
    def build_date(self):
        return parse_date_string(self.build_date_str)
