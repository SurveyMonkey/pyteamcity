import datetime
import json

import responses

from pyteamcity.future import PageJoiner, TeamCity


tc = TeamCity()


@responses.activate
def test_unit_PageJoiner():
    response1_json = {
        u'count': 5,
        u'href': u'/guestAuth/app/rest/builds/?locator=sinceDate:20160807T231459%2B0000,count:5',  # noqa: E501
        u'nextHref': u'/guestAuth/app/rest/builds/?locator=count:5,start:5,sinceDate:20160807T231459%2B0000',  # noqa: E501
        u'build': [{u'status': u'FAILURE', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474539&buildTypeId=Teamcity_DeployBuildAgents', u'number': u'578', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474539', u'branchName': u'master', u'buildTypeId': u'Teamcity_DeployBuildAgents', u'id': 1474539}, {u'status': u'SUCCESS', u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474538&buildTypeId=Teamcity_TriggerFullBackup', u'number': u'561', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474538', u'buildTypeId': u'Teamcity_TriggerFullBackup', u'id': 1474538}, {u'status': u'FAILURE', u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474537&buildTypeId=DevOps_Infra_Mt', u'number': u'424', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474537', u'buildTypeId': u'DevOps_Infra_Mt', u'id': 1474537}, {u'status': u'FAILURE', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474530&buildTypeId=Teamcity_DeployBuildAgents', u'number': u'577', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474530', u'branchName': u'master', u'buildTypeId': u'Teamcity_DeployBuildAgents', u'id': 1474530}, {u'status': u'SUCCESS', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474528&buildTypeId=Dummysvc_Branches_Version', u'number': u'155', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474528', u'branchName': u'master', u'buildTypeId': u'Dummysvc_Branches_Version', u'id': 1474528}]}  # noqa: E501
    response2_json = {
        u'count': 5,
        u'prevHref': u'/guestAuth/app/rest/builds/?locator=count:5,start:0,sinceDate:20160807T231459%2B0000',  # noqa: E501
        u'href': u'/guestAuth/app/rest/builds/?locator=count:5,start:5,sinceDate:20160807T231459%2B0000',  # noqa: E501
        u'build': [{u'status': u'SUCCESS', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474524&buildTypeId=Dummysvc_Branches_Version', u'number': u'153', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474524', u'branchName': u'master', u'buildTypeId': u'Dummysvc_Branches_Version', u'id': 1474524}, {u'status': u'FAILURE', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474521&buildTypeId=Dummysvc_Branches_Py27', u'number': u'148', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474521', u'branchName': u'master', u'buildTypeId': u'Dummysvc_Branches_Py27', u'id': 1474521}, {u'status': u'FAILURE', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474517&buildTypeId=Dummysvc_Branches_Py27', u'number': u'148', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474517', u'branchName': u'master', u'buildTypeId': u'Dummysvc_Branches_Py27', u'id': 1474517}, {u'status': u'SUCCESS', u'defaultBranch': True, u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474510&buildTypeId=Dummysvc_Branches_Version', u'number': u'148', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474510', u'branchName': u'master', u'buildTypeId': u'Dummysvc_Branches_Version', u'id': 1474510}, {u'status': u'SUCCESS', u'webUrl': u'https://teamcity.corp.surveymonkey.com/viewLog.html?buildId=1474509&buildTypeId=Teamcity_TriggerFullBackup', u'number': u'560', u'state': u'finished', u'href': u'/guestAuth/app/rest/builds/id:1474509', u'buildTypeId': u'Teamcity_TriggerFullBackup', u'id': 1474509}]}  # noqa: E501

    def request_callback(request):
        if 'start:5' in request.path_url:
            return (200, {}, json.dumps(response2_json))
        else:
            return (200, {}, json.dumps(response1_json))

    responses.add_callback(
        responses.GET,
        tc.relative_url('app/rest/builds/'),
        # json=response1_json, status=200,
        callback=request_callback,
        content_type='application/json',
    )

    date = datetime.datetime.now() - datetime.timedelta(days=7)
    builds = PageJoiner(
        tc.builds.all().filter(since_date=date, count=5))

    cnt = 0
    for build in builds:
        cnt += 1

    assert cnt == len(builds) == 10

    assert '/app/rest/builds/' in builds.url
