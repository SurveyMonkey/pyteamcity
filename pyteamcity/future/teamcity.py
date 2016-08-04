import os

import requests

from .core.manager import Manager

from .agent import AgentQuerySet
from .agent_pool import AgentPoolQuerySet
from .build import BuildQuerySet
from .build_type import BuildTypeQuerySet
from .project import ProjectQuerySet
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
