"""
pyteamcity/legacy/legacy.py

This is the legacy API and will probably not be maintained going forward.

Before using this or making changes to this file, be sure to have a look at
`pyteamcity/future`.

RESTful api definition: http://${TeamCity}/guestAuth/app/rest/application.wadl
"""

import collections
import inspect
import os
import re
import textwrap
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
import requests


class ConnectionError(Exception):
    def __init__(self, host, port, orig_exception=None):
        self.host = host
        self.port = port
        self.orig_exception = orig_exception

    def __str__(self):
        return 'Failed to connect to %s:%s' % (self.host, self.port)


class HTTPError(Exception):
    url = None
    status_code = None

    def __init__(self, msg, url, status_code):
        super(HTTPError, self).__init__(msg)
        self.url = url
        self.status_code = status_code


def _underscore_to_camel_case(s):
    words = s.split('_')
    words = [words[0].lower()] + [w.title() for w in words[1:]]
    return ''.join(words)


def _build_url(*args, **kwargs):
    """Builds a new API url from scratch."""
    parts = [kwargs.get('base_url')]
    parts.extend(args)
    parts = [str(p) for p in parts]
    return '/'.join(parts)


def get_default_kwargs(func):
    """Returns a sequence of tuples (kwarg_name, default_value) for func"""
    argspec = inspect.getargspec(func)
    if not argspec.defaults:
        return []
    return zip(argspec.args[-len(argspec.defaults):],
               argspec.defaults)


def endpoint(url_pattern, method='GET'):
    def wrapped_func(f):
        def get_url(*args, **kwargs):
            # kwargs with default values declared by function
            all_kwargs = dict(get_default_kwargs(f))

            # kwargs for positional arguments passed by caller
            groups = re.findall('{(\w+)}', url_pattern)
            all_kwargs.update(dict(zip(groups, args)))

            # kwargs for keyword arguments passed by caller
            all_kwargs.update(kwargs)

            return _build_url(url_pattern.format(*args, **all_kwargs),
                              **all_kwargs)

        def inner_func(self, *args, **kwargs):
            kwargs['base_url'] = self.base_url
            url = get_url(*args, **kwargs)
            request = self._get_request('GET', url)
            return_type = kwargs.get('return_type', 'data')
            if return_type == 'url':
                return url
            if return_type == 'request':
                return request
            if method == 'GET':
                response = self._get(url)
            elif method == 'POST':
                response = self._post(url)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError:
                raise HTTPError(response.text,
                                url=url,
                                status_code=response.status_code)
            try:
                if response.headers['Content-Type'] == 'application/json':
                    return response.json()
                else:
                    return response.content
            except Exception as e:
                return response.text
        return inner_func
    return wrapped_func


def GET(url_pattern):
    return endpoint(url_pattern, method='GET')


def POST(url_pattern):
    return endpoint(url_pattern, method='POST')


class TeamCity:
    username = None
    password = None
    server = None
    port = None
    error_handler = None

    def __init__(self, username=None, password=None, server=None, port=None,
                 session=None, protocol=None):
        self.username = username or os.getenv('TEAMCITY_USER')
        self.password = password or os.getenv('TEAMCITY_PASSWORD')
        self.host = server or os.getenv('TEAMCITY_HOST')
        self.port = port or int(os.getenv('TEAMCITY_PORT', 0)) or 80
        self.protocol = protocol or os.getenv('TEAMCITY_PROTOCOL', 'http')
        self.base_base_url = "%s://%s:%d" % (
            self.protocol, self.host, self.port)
        self.guest_auth_base_url = "%s://%s:%d/guestAuth" % (
            self.protocol, self.host, self.port)
        if self.username and self.password:
            self.base_url = "%s://%s:%d/httpAuth/app/rest" % (
                self.protocol, self.host, self.port)
            self.auth = (self.username, self.password)
        else:
            self.base_url = "%s://%s:%d/guestAuth/app/rest" % (
                self.protocol, self.host, self.port)
            self.auth = None
        self.session = session or requests.Session()
        self._agent_cache = {}

    def get_url(self, path):
        return '/'.join([self.base_base_url, path])

    def _get_request(self, verb, url, headers=None, **kwargs):
        if headers is None:
            headers = {'Accept': 'application/json'}
        return requests.Request(
            verb,
            url,
            auth=self.auth,
            headers=headers,
            **kwargs).prepare()

    def _get(self, url, **kwargs):
        request = self._get_request('GET', url, **kwargs)
        return self._send_request(request)

    def _post(self, url, **kwargs):
        request = self._get_request('POST', url, **kwargs)
        return self._send_request(request)

    def _put(self, url, **kwargs):
        request = self._get_request('PUT', url, **kwargs)
        return self._send_request(request)

    def _send_request(self, request):
        try:
            return self.session.send(request)
        except requests.exceptions.ConnectionError as e:
            new_exception = ConnectionError(self.host, self.port, e)
            if self.error_handler:
                self.error_handler(new_exception)
            else:
                raise new_exception

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

    def get_builds(self,
                   build_type_id='', branch='', status='', running='',
                   tags=None,
                   user=None, project='', pinned=None,
                   since_build=None, until_build=None, since_date=None, until_date=None,
                   start=0, count=100, **kwargs):
        _get_locator_kwargs = {}
        if branch:
            _get_locator_kwargs['branch'] = branch
        if build_type_id:
            _get_locator_kwargs['build_type'] = build_type_id
        if status:
            _get_locator_kwargs['status'] = status
        if running:
            _get_locator_kwargs['running'] = running
        if tags:
            _get_locator_kwargs['tags'] = tags
        if user:
            _get_locator_kwargs['user'] = user
        if project:
            _get_locator_kwargs['project'] = project
        if pinned is not None:
            _get_locator_kwargs['pinned'] = pinned
        if since_build:
            _get_locator_kwargs['since_build'] = since_build
        if until_build:
            _get_locator_kwargs['until_build'] = until_build
        if since_date:
            _get_locator_kwargs['since_date'] = since_date
        if until_date:
            _get_locator_kwargs['until_date'] = until_date


        locator = self._get_locator(**_get_locator_kwargs)

        if locator:
            return self._get_all_builds_locator(
                locator=locator,
                start=start, count=count,
                **kwargs)
        else:
            return self._get_all_builds(
                start=start, count=count,
                **kwargs)

    def _get_locator(self, **kwargs):
        if not kwargs:
            return ''

        # Sort kwargs.items() so that ordering is deterministic, which is very
        # handy for automated tests
        return ','.join('%s:%s' % (_underscore_to_camel_case(k), v)
                        for k, v in sorted(kwargs.items()) if v)

    @GET('builds/?start={start}&count={count}')
    def _get_all_builds(self, start=0, count=100):
        """
        Gets all builds in the TeamCity server pointed to by this instance of
        the Client.
        This can be very large since it is historic data. Therefore the count
        can be limited.

        :param start: what build number to start from
        :param count: how many builds to return
        """

    @GET('builds/?locator={locator}&start={start}&count={count}')
    def _get_all_builds_locator(self, locator='', start=0, count=100):
        """
        Gets all builds in the TeamCity server pointed to by this instance of
        the Client.
        This can be very large since it is historic data. Therefore the count
        can be limited.

        :param start: what build number to start from
        :param count: how many builds to return
        """

    @GET('builds/id:{build_id}')
    def get_build_by_build_id(self, build_id):
        """
        Gets a build with build ID `bId`.

        :param build_id: the build to get, in the format [0-9]+
        """

    @GET('changes?start={start}&count={count}')
    def get_all_changes(self, start=0, count=10):
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

    def get_build_types(self, project='', affected_project='',
                        template_flag=None,
                        **kwargs):
        """
        Gets all build types in the TeamCity server pointed to by this instance
        of the Client.
        """
        _get_locator_kwargs = {}
        if project:
            _get_locator_kwargs['project'] = project
        if affected_project:
            _get_locator_kwargs['affected_project'] = affected_project
        if template_flag:
            _get_locator_kwargs['template_flag'] = template_flag

        locator = self._get_locator(**_get_locator_kwargs)

        if locator:
            return self._get_all_build_types_locator(
                locator=locator,
                **kwargs)
        else:
            return self._get_all_build_types(**kwargs)

    @GET('buildTypes/?locator={locator}')
    def _get_all_build_types_locator(self, locator=''):
        """
        Gets all build types in the TeamCity server pointed to by this instance
        of the Client.
        """

    @GET('buildTypes/')
    def _get_all_build_types(self):
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

    def get_projects(self, parent_project_id=None, **kwargs):
        return_type = kwargs.get('return_type')
        all_projects_data = self._get_all_projects(**kwargs)

        if parent_project_id is None or return_type in ('url', 'request'):
            return all_projects_data

        projects = [project for project in all_projects_data['project']
                    if parent_project_id == project.get('parentProjectId')]
        ret = {'count': len(projects),
               'project': projects}
        return ret

    @GET('buildQueue')
    def get_queued_builds(self):
        """
        Gets queued builds
        """

    @GET('buildQueue/id:{build_id}')
    def get_queued_build_by_build_id(self, build_id):
        """
        Gets a queued build with build ID `build_id`.

        :param build_id: the build to get, in the format [0-9]+
        """

    def trigger_build(
            self,
            build_type_id, branch=None,
            comment=None, parameters=None, agent_id=None):
        """
        Trigger a new build
        """
        url = _build_url('buildQueue', base_url=self.base_url)
        data = self._get_build_node(
            build_type_id, branch,
            comment, parameters, agent_id)

        response = self._post(
            url,
            headers={'Content-Type': 'application/xml'},
            data=data)

        root = ET.fromstring(response.text)
        new_build_attributes = root.findall('.')[0].attrib
        return new_build_attributes

    def _get_build_node(
            self,
            build_type_id, branch=None,
            comment=None, parameters=None, agent_id=None):
        build_attributes = ''

        if branch:
            build_attributes = 'branchName="%s"' % branch

        if build_attributes:
            data = '<build %s>\n' % build_attributes
        else:
            data = '<build>\n'

        data += '    <buildType id="%s"/>\n' % build_type_id

        if agent_id:
            data += '    <agent id="%s"/>\n' % agent_id

        if comment:
            data += '    <comment><text>%s</text></comment>\n' % comment

        if parameters:
            data += '    <properties>\n'
            data += ''.join([
                '        <property name="%s" value="%s"/>\n' % (name, value)
                for name, value in parameters.items()])
            data += '    </properties>\n'

        data += '</build>\n'

        return data

    @GET('projects')
    def _get_all_projects(self):
        """
        Gets all projects in the TeamCity server pointed to by this instance of
        the Client.
        """

    def create_project(self, name):
        """
        Create project
        """
        url = _build_url('projects', base_url=self.base_url)
        data = {'name': name}
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
        return self.session.post(url, json=data, headers=headers)

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

    @GET('agents/name:{agent_name}')
    def get_agent_by_agent_name(self, agent_name):
        """
        Gets details for an agent with name `agent_name`.

        :param agent_name: the agent name to get
        """

    def get_agent_statistics(self):
        counters = collections.Counter()
        counters['by_build_type'] = collections.Counter()

        for agent in self.get_agents()['agent']:
            counters['num_total'] += 1
            build_text = self.get_agent_build_type(agent['id'])
            counters['by_build_type'][build_text] += 1
            if 'Idle' in build_text:
                counters['num_idle'] += 1
            else:
                counters['num_busy'] += 1

        return counters


    def get_agent_build_type(self, agent_id):
        data = self._fetch_agent_details(agent_id)
        return data['build_type']

    def get_agent_build_text(self, agent_id):
        data = self._fetch_agent_details(agent_id)
        return data['build_text']

    def _fetch_agent_details(self, agent_id):
        data = self._agent_cache.get(agent_id)
        if data:
            return data

        url = self.get_url('/agentDetails.html?id=%s' % agent_id)
        agent_details_response = self._get(url)
        html_doc = agent_details_response.text
        if 'Running build' not in html_doc:
            build_type = build_text = 'Idle'
        else:
            soup = BeautifulSoup(html_doc)
            build_type_node = soup.find(class_='buildTypeName')
            build_text_node = soup.find(id=re.compile('build:(?P<build_type>\d+):text'))
            build_type = build_type_node.text.replace('\n', '').replace('\r', '')
            build_text = build_text_node.text
        data = {
            'build_type': build_type,
            'build_text': build_text,
        }
        self._agent_cache[agent_id] = data
        return data

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

    @GET('builds/id:{build_id}/resulting-properties')
    def get_build_parameters_by_build_id(self, build_id):
        """
        Gets parameters for a build with ID `build_id`.

        :param build_id: the build ID to get, in format [0-9]+
        """

    @GET('builds/id:{build_id}/artifacts/{data_type}/{artifact_relative_name}')
    def get_build_artifacts_by_build_id(self, build_id, data_type, artifact_relative_name):
        """
        Gets artifacts for a build with ID `build_id`.

        :param build_id: the build ID to get, in format [0-9]+
        """

    def get_build_log_by_build_id(self, build_id):
        """
        Gets log for a build with ID `build_id`.

        :param build_id: the build ID to get, in format [0-9]+
        """
        url = _build_url(
            'downloadBuildLog.html?buildId={build_id}'.format(
                build_id=build_id),
            base_url=self.guest_auth_base_url)
        return self._get(url)

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

    def get_project_params(self, proj_id):
        """Returns project parameters dictionary with values """
        project = self.get_project_by_project_id(proj_id)
        proj_params = dict([(x['name'], x.get('value'))
                            for x in project['parameters']['property']])
        return proj_params

    def reset_build_counter(self, build_type_id, counter=0):
        """ Resets the build types build counter """
        url = _build_url(
            'buildTypes',
            'id:{build_type_id}'.format(build_type_id = build_type_id),
            'settings',
            'buildNumberCounter',
            base_url= self.base_url)
        return self.session.put(
            url=url,
            auth=(self.username, self.password),
            data=str(counter))

    @GET('testOccurrences?locator=test:{test_locator}')
    def get_test(self, test_locator):
        """
        Gets individual test history

        :param test_locator: test id
        """
