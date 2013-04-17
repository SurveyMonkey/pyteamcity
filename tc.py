
"""
RESTful api definition: http://${TeamCity}/guestAuth/app/rest/application.wadl
"""

import json
import urllib2
import base64
from datetime import datetime,timedelta
import pprint

class TeamCityRESTApiClient:

    def __init__(self, username, password, server, port):
        self.TC_REST_URL = "http://%s:%d/httpAuth/app/rest/" % (server, port)
        self.userpass = '%s:%s' % (username, password)
        self.locators = {}

    # count:<number> - serve only the specified number of builds
    def set_count(self, count):
        self.locators['count'] = count
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
        minutes_delta = timedelta(minutes = minutes)
        minutes_ago = datetime.now() - minutes_delta

	    # Hardcoding NY time zone here... Assumes machines is on the same timezone
        self.locators['sinceDate'] = minutes_ago.strftime('%Y%m%dT%H%M%S') + '-0500'
        return self

    # start:<number> - list the builds from the list starting from the position specified (zero-based)
    def set_start(self, start):
        self.locators['start'] = start
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
        full_resource_url = self.resource
        if len(self.locators) > 0:
            # print self.locators
            locators ='?locator=' + ','.join(["%s:%s" % (k, v) for k, v in self.locators.iteritems()])
            full_resource_url = full_resource_url + locators
        return full_resource_url

    def get_from_server(self):
        full_resource_url = self.compose_resource_path()
        print full_resource_url
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
        return self.set_resource('server')

    def get_all_plugins(self):
        return self.set_resource('server/plugins')

    def get_all_builds(self):
        return self.set_resource('builds')

    # btId = bt[0-9]+
    def get_all_builds_by_build_type_id(self, btId,start=0,count=100):
        return self.set_resource('buildTypes/id:%s/builds/?count=%d&start=%d' % (btId,count,start))

    # bId = [0-9]+
    def get_build_by_build_id(self, bId):
        return self.set_resource('builds/id:%s' % bId)

    def get_all_changes(self):
        return self.set_resource('changes')

    def get_change_by_change_id(self, cId):
        return self.set_resource('changes/id:%s' % cId)

    # bId = [0-9]+
    def get_changes_by_build_id(self, bId):
        return self.set_resource('changes?build=id:%s' % bId)

    def get_all_build_types(self):
        return self.set_resource('buildTypes')

    # btId = bt[0-9]+
    def get_build_type(self, btId):
        return self.set_resource('buildTypes/id:%s' % btId)

    def get_all_projects(self):
        return self.set_resource('projects')

    # pid = project[0-9]+
    def get_project_by_project_id(self, pId):
        return self.set_resource('projects/id:%s' % pId)

    def get_agents(self):
        return self.set_resource('agents')

    # aId = [0-9]+
    def get_agent_by_agent_id(self, aId):
        return self.set_resource('agents/id:%d' % aId)

    def get_build_statistics_by_build_id(self, bId):
        return self.set_resource('builds/id:%s/statistics' % bId)

    def get_build_tags_by_build_id(self, bId):
        return self.set_resource('builds/id:%s/tags' % bId)

    def get_all_vcs_roots(self):
        return self.set_resource('vcs-roots')

    def get_vcs_root_by_vcs_root_id(self, vrId):
        return self.set_resource('vcs-roots/id:%s' % vrId)

    def get_all_users(self):
        return self.set_resource('users')

