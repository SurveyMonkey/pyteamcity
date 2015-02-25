"""
RESTful api definition: http://${TeamCity}/guestAuth/app/rest/application.wadl
"""

import os
import re

import requests


def _build_url(*args, **kwargs):
    """Builds a new API url from scratch."""
    parts = [kwargs.get('base_url')]
    parts.extend(args)
    parts = [str(p) for p in parts]
    return '/'.join(parts)


def GET(url_pattern):
    def wrapped_func(f):
        def get_url(*args, **kwargs):
            groups = re.findall('{(\w+)}', url_pattern)
            for arg, group in zip(args, groups):
                kwargs[group] = arg
            return _build_url(url_pattern.format(*args, **kwargs), **kwargs)

        def inner_func(self, *args, **kwargs):
            kwargs['base_url'] = self.base_url
            url = get_url(*args, **kwargs)
            request = self._get_request('GET', url)
            return_type = kwargs.get('return_type', 'data')
            if return_type == 'url':
                return url
            if return_type == 'request':
                return request
            response = self._get(url)
            # import pdb; pdb.set_trace()
            return response.json()
        return inner_func
    return wrapped_func


class TeamCity:
    def __init__(self, username=None, password=None, server=None, port=None, session=None):
        self.username = username or os.getenv('TEAMCITY_USER')
        self.password = password or os.getenv('TEAMCITY_PASSWORD')
        self.host = server or os.getenv('TEAMCITY_HOST')
        self.port = port or int(os.getenv('TEAMCITY_PORT', 0)) or 80
        self.base_url = "http://%s:%d/httpAuth/app/rest" % (self.host, self.port)
        self.locators = {}
        self.parameters = {}
        self.session = session or requests.Session()

    def _build_url(self, *args, **kwargs):
        """Builds a new API url from scratch."""
        parts = [kwargs.get('base_url') or self.base_url]
        parts.extend(args)
        parts = [str(p) for p in parts]
        return '/'.join(parts)

    def _get_request(self, verb, url, **kwargs):
        return requests.Request(
            verb,
            url,
            auth=(self.username, self.password),
            headers={'Accept': 'application/json'}).prepare()

    def _get(self, url, **kwargs):
        request = self._get_request('GET', url, **kwargs)
        return self.session.send(request)

    @GET('server')
    def get_server_info(self):
        """
        Gets server info of the TeamCity server pointed to by this instance of
        the Client.
        """

    @GET('server/plugins')
    def get_all_plugins(self):
        """
        Gets all plugins in the TeamCity server pointed to by this instance of
        the Client.
        """

    @GET('builds/?start={start}&count={count}')
    def get_all_builds(self, start=0, count=100):
        """
        Gets all builds in the TeamCity server pointed to by this instance of
        the Client.
        This can be very large since it is historic data. Therefore the count
        can be limited.

        :param start: what build number to start from
        :param count: how many builds to return
        """

    @GET('buildTypes/id:{build_type_id}/builds/?start={start}&count={count}')
    def get_all_builds_by_build_type_id(self, build_type_id, start=0, count=100):
        """
        Gets all builds of a build type build type id `btId`.
        This can be very large since it is historic data. Therefore the count
        can be limited.

        :param build_type_id: the build type to get builds from, in the format
        bt[0-9]+
        :param start: what build number to start from
        :param count: how many builds to return
        """

    @GET('builds/id:{build_id}')
    def get_build_by_build_id(self, build_id):
        """
        Gets a build with build ID `bId`.

        :param build_id: the build to get, in the format [0-9]+
        """

    @GET('changes')
    def get_all_changes(self):
        """
        Gets all changes made in the TeamCity server pointed to by this
        instance of the Client.
        """

    @GET('changes/id:{change_id}')
    def get_change_by_change_id(self, change_id):
        """
        Gets a particular change with change ID `cId`.

        :param change_id: the change to get, in the format [0-9]+
        """

    @GET('changes/build:id:{build_id}')
    def get_changes_by_build_id(self, build_id):
        """
        Gets changes in a build for a build ID `build_id`.

        :param build_id: the build to get changes of in the format [0-9]+
        """

    @GET('buildTypes')
    def get_all_build_types(self):
        """
        Gets all build types in the TeamCity server pointed to by this instance
        of the Client.
        """

    @GET('buildTypes/id:{build_type_id}')
    def get_build_type(self, build_type_id):
        """
        Gets details for a build type with id `build_type_id`.

        :param build_type_id: the build type to get, in format bt[0-9]+
        """

    @GET('projects')
    def get_all_projects(self):
        """
        Gets all projects in the TeamCity server pointed to by this instance of
        the Client.
        """

    @GET('projects/id:{project_id}')
    def get_project_by_project_id(self, project_id):
        """
        Gets details for a project with ID `project_id`.

        :param project_id: the project ID to get, in format project[0-9]+
        """

    @GET('agents')
    def get_agents(self):
        """
        Gets all agents in the TeamCity server pointed to by this instance of
        the Client.
        """

    @GET('agents/id:{agent_id}')
    def get_agent_by_agent_id(self, agent_id):
        """
        Gets details for an agent with ID `agent_id`.

        :param agent_id: the agent ID to get, in format [0-9]+
        """

    @GET('builds/id:{build_id}/statistics')
    def get_build_statistics_by_build_id(self, build_id):
        """
        Gets statistics for a build with ID `build_id`.
        Statistics include `BuildDuration`, `FailedTestCount`,
        `TimeSpentInQueue`, and more.

        :param build_id: the build ID to get, in format [0-9]+
        """

    @GET('builds/id:{build_id}/tags')
    def get_build_tags_by_build_id(self, build_id):
        """
        Gets tags for a build with ID `build_id`.

        :param build_id: the build ID to get, in format [0-9]+
        """

    @GET('vcs-roots')
    def get_all_vcs_roots(self):
        """
        Gets all VCS roots in the TeamCity server pointed to by this instance
        of the Client.
        """

    @GET('vcs-roots/id:{vcs_root_id}')
    def get_vcs_root_by_vcs_root_id(self, vcs_root_id):
        """
        Gets a VCS root with the specified ID `vcs_root_id`.

        :param vcs_root_id: the VCS root to get
        """

    @GET('users')
    def get_all_users(self):
        """
        Gets all users in the TeamCity server pointed to by this instance of
        the Client.
        """

    @GET('users/username:{username}')
    def get_user_by_username(self, username):
        """
        Gets user details for a given username.

        :param username: the username to get details for.
        """
