"""
RESTful api definition: http://${TeamCity}/guestAuth/app/rest/application.wadl
"""

import json
import urllib2
import base64
from datetime import datetime, timedelta


class TeamCityRESTApiClient:
    def __init__(self, username, password, server, port):
        self.TC_REST_URL = "http://%s:%d/httpAuth/app/rest/" % (server, port)
        self.userpass = '%s:%s' % (username, password)
        self.locators = {}
        self.parameters = {}


    # count:<number> - serve only the specified number of builds
    def set_count(self, count):
        """

        :param count:
        :return:
        """
        self.parameters['count'] = count
        return self

    # running:<true/false/any> - limit the builds by running flag.
    def set_running(self, running):
        self.locators['running'] = running
        return self


    # buildType:(<buildTypeLocator>) - only the builds of the specified build configuration
    def set_build_type(self, bt):
        self.locators['buildType'] = bt
        return self


    # tags:<tags> - ","(comma) -delimited list of build tags (only builds containing all the specified tags are returned)
    def set_tags(self, tags):
        self.locators['tags'] = tags
        return self


    # status:<SUCCESS/FAILURE/ERROR> - list the builds with the specified status only
    def set_status(self, status):
        self.locators['status'] = status
        return self


    # user:(<userLocator>) - limit the builds to only those triggered by user specified
    def set_user(self, user):
        self.locators['user'] = user
        return self


    # personal:<true/false/any> - limit the builds by personal flag.
    def set_personal(self, personal):
        self.locators['personal'] = personal
        return self


    # canceled:<true/false/any> - limit the builds by canceled flag.
    def set_canceled(self, canceled):
        self.locators['canceled'] = canceled
        return self


    # pinned:<true/false/any> - limit the builds by pinned flag.
    def set_pinned(self, pinned):
        self.locators['pinned'] = pinned
        return self


    # branch:<branch locator> - since TeamCity 7.1 limit the builds by branch. <branch locator> can be branch name (displayed in UI, or "(name:<name>,default:<true/false/any>,unspecified:<true/false/any>,branched:<true/false/any>)". If not specified, only builds from default branch are returned.
    def set_branch(self, branch):
        self.locators['branch'] = branch
        return self


    # agentName:<name> - agent name to return only builds ran on the agent with name specified
    def set_agent_name(self, agent_name):
        self.locators['agentName'] = agent_name
        return self


    # sinceBuild:(<buildLocator>) - limit the list of builds only to those after the one specified
    def set_since_build(self, since_build):
        self.locators['sinceBuild'] = since_build
        return self


    # sinceDate:<date> - limit the list of builds only to those started after the date specified. The date should in the same format as dates returned by REST API.
    def set_since_date(self, minutes):
        minutes_delta = timedelta(minutes=minutes)
        minutes_ago = datetime.now() - minutes_delta

        # Hardcoding NY time zone here... Assumes machines is on the same timezone
        self.locators['sinceDate'] = minutes_ago.strftime('%Y%m%dT%H%M%S') + '-0500'
        return self


    # start:<number> - list the builds from the list starting from the position specified (zero-based)
    def set_start(self, start):
        self.parameters['start'] = start
        return self


    # lookupLimit:<number> - since TeamCity 7.0 limit processing to the latest N builds only. If none of the latest N builds match other specified criteria of the build locator, 404 response is returned.
    def set_lookup_limit(self, lookup_limit):
        self.locators['lookupLimit'] = lookup_limit
        return self


    def set_tc_server(self, url, port):
        self.TC_REST_URL = "http://%s:%s/httpAuth/app/rest/" % (url, port)
        return self


    def set_resource(self, resource):
        self.resource = self.TC_REST_URL + resource
        return self


    def compose_resource_path(self):
        """
        Creates the URL by appending the resource, locators, and arguments in the appropriate places.

        :return: the well-built URL to make the request with.
        """
        full_resource_url = self.resource
        if self.locators:
            locators = 'locator=' + ','.join([
                "%s:%s" % (k, v)
                for k, v in self.locators.iteritems()
            ])
        else:
            locators = ''
        get_args = '&'.join([locators] + [
            '%s=%s' % (k, v)
            for k, v in self.parameters.iteritems()
        ])
        if get_args:
            full_resource_url = full_resource_url + '?' + get_args
        return full_resource_url

    def get_from_server(self):
        """
        Makes a request to the TeamCity server pointed to by this instance of the Client.
        Uses httpAuth and accepts a JSON return.

        Then it creates a Python dictionary by loading in the JSON.

        :return: the Python dictionary which represents the JSON response.
        """
        full_resource_url = self.compose_resource_path()
        req = urllib2.Request(full_resource_url)
        base64string = base64.encodestring(self.userpass).replace('\n', '')
        req.add_header("Authorization", "Basic %s" % base64string)
        req.add_header('Accept', 'application/json')
        response = urllib2.urlopen(req)
        res = response.read()
        data = json.loads(res)
        response.close()
        return data


    def get_server_info(self):
        """
        Gets server info of the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/server`.
        """
        return self.set_resource('server')


    def get_all_plugins(self):
        """
        Gets all plugins in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/server/plugins`.
        """
        return self.set_resource('server/plugins')


    def get_all_builds(self, start=0, count=100):
        """
        Gets all builds in the TeamCity server pointed to by this instance of the Client.
        This can be very large since it is historic data. Therefore the count can be limited.

        :param start: what build number to start from
        :param count: how many builds to return
        :return: an instance of the Client with `resource = <url>/builds/?start=<start>&count=<count>`.
        """
        self.set_start(start)
        self.set_count(count)
        return self.set_resource('builds/')

    def get_all_builds_by_build_type_id(self, btId, start=0, count=100):
        """
        Gets all builds of a build type build type id `btId`.
        This can be very large since it is historic data. Therefore the count can be limited.

        :param btId: the build type to get builds from, in the format bt[0-9]+
        :param start: what build number to start from
        :param count: how many builds to return
        :return: an instance of the Client with `resource = <url>/buildTypes/id:<btId>/builds/?start=<start>&count=<count>`.
        """
        self.set_count(count)
        self.set_start(start)
        return self.set_resource('buildTypes/id:%s/builds/' % (btId))

    def get_build_by_build_id(self, bId):
        """
        Gets a build with build ID `bId`.

        :param bId: the build to get, in the format [0-9]+
        :return: an instance of the Client with `resource = <url>/builds/id:<bId>`.
        """
        return self.set_resource('builds/id:%s' % bId)

    def get_all_changes(self):
        """
        Gets all changes made in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/changes`.
        """
        return self.set_resource('changes')

    def get_change_by_change_id(self, cId):
        """
        Gets a particular change with change ID `cId`.

        :param cId: the change to get, in the format [0-9]+
        :return: an instance of the Client with `resource = <url>/changes/id:<cId>`.
        """
        return self.set_resource('changes/id:%s' % cId)


    def get_changes_by_build_id(self, bId):
        """
        Gets changes in a build for a build ID `bId`.

        :param bId: the build to get changes of in the format [0-9]+
        :return: an instance of the Client with `resource = <url>/changes/build:id:<bId>`.
        """
        self.parameters['build'] = 'id:%s' % (bId)
        return self.set_resource('changes')

    def get_all_build_types(self):
        """
        Gets all build types in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/buildTypes`.
        """
        return self.set_resource('buildTypes')

    def get_build_type(self, btId):
        """
        Gets details for a build type with id `btId`.

        :param btId: the build type to get, in format bt[0-9]+
        :return: an instance of the Client with `resource = <url>/buildTypes/id:<btId>`
        """
        return self.set_resource('buildTypes/id:%s' % btId)

    def get_all_projects(self):
        """
        Gets all projects in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/projects`
        """
        return self.set_resource('projects')

    def get_project_by_project_id(self, pId):
        """
        Gets details for a project with ID `pId`.

        :param pId: the project ID to get, in format project[0-9]+
        :return: an instance of the Client with `resource = <url>/projects/id:<pId>`
        """
        return self.set_resource('projects/id:%s' % pId)

    def get_agents(self):
        """
        Gets all agents in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/agents`
        """
        return self.set_resource('agents')


    def get_agent_by_agent_id(self, aId):
        """
        Gets details for an agent with ID `aId`.

        :param aId: the agent ID to get, in format [0-9]+
        :return: an instance of the Client with `resource = <url>/agents/id:<aId>`
        """
        return self.set_resource('agents/id:%d' % aId)

    def get_build_statistics_by_build_id(self, bId):
        """
        Gets statistics for a build with ID `bId`.
        Statistics include `BuildDuration`, `FailedTestCount`, `TimeSpentInQueue`, and more.

        :param bId: the build ID to get, in format [0-9]+
        :return: an instance of the Client with `resource = <url>/builds/id:<bId>/statistics`
        """
        return self.set_resource('builds/id:%s/statistics' % bId)

    def get_build_tags_by_build_id(self, bId):
        """
        Gets tags for a build with ID `bId`.

        :param bId: the build ID to get, in format [0-9]+
        :return: an instance of the Client with `resource = <url>/builds/id:<bId>/tags`
        """
        return self.set_resource('builds/id:%s/tags' % bId)

    def get_all_vcs_roots(self):
        """
        Gets all VCS roots in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/vcs-roots`
        """
        return self.set_resource('vcs-roots')

    def get_vcs_root_by_vcs_root_id(self, vrId):
        """
        Gets a VCS root with the specified ID `vrId`.

        :param vrId: the VCS root to get
        :return: an instance of the Client with `resource = <url>/vcs-roots/id:<vrId>`
        """
        return self.set_resource('vcs-roots/id:%s' % vrId)

    def get_all_users(self):
        """
        Gets all users in the TeamCity server pointed to by this instance of the Client.

        :return: an instance of the Client with `resource = <url>/users`
        """
        return self.set_resource('users')

    def get_user_by_username(self, username):
        """
        Gets user details for a given username.

        :param username: the username to get details for.
        :return: an instance of the Client with `resource = <url>/users/username:<username>`
        """
        return self.set_resource('users/username:%s' % username)
