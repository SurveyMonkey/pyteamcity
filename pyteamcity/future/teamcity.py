import os

import requests

from .core.manager import Manager
from .core.utils import parse_date_string

from .agent import AgentQuerySet
from .agent_pool import AgentPoolQuerySet
from .build import BuildQuerySet
from .build_type import BuildTypeQuerySet
from .project import ProjectQuerySet
from .queued_build import QueuedBuildQuerySet
from .user import UserQuerySet
from .user_group import UserGroupQuerySet
from .vcs_root import VCSRootQuerySet


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

    @property
    def server_info(self):
        url = self.base_url + '/app/rest/server'
        res = self.session.get(url)
        res.raise_for_status()
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
