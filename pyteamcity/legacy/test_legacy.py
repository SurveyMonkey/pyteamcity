import json

import mock
import pytest
import requests

from pyteamcity import TeamCity, HTTPError

user = 'TEAMCITY_USER'
password = 'TEAMCITY_PASSWORD'
host = 'TEAMCITY_HOST'
port = 4567

tc = TeamCity(user, password, host, port)


def test_get_all_users():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/users'
    url = tc.get_all_users(return_type='url')
    assert url == expected_url

    req = tc.get_all_users(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_user_by_username():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'users/username:codyw')
    url = tc.get_user_by_username('codyw', return_type='url')
    assert url == expected_url

    req = tc.get_user_by_username('codyw', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_vcs_roots():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/vcs-roots'
    url = tc.get_all_vcs_roots(return_type='url')
    assert url == expected_url

    req = tc.get_all_vcs_roots(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_vcs_root_by_vcs_root_id():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'vcs-roots/id:41')
    url = tc.get_vcs_root_by_vcs_root_id(41, return_type='url')
    assert url == expected_url

    req = tc.get_vcs_root_by_vcs_root_id(41, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_agents():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/agents'
    url = tc.get_agents(return_type='url')
    assert url == expected_url

    req = tc.get_agents(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_agent_by_agent_id():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/agents/id:41'
    url = tc.get_agent_by_agent_id(41, return_type='url')
    assert url == expected_url

    req = tc.get_agent_by_agent_id(41, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_agent_by_agent_name():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/agents/name:test'
    url = tc.get_agent_by_agent_name('test', return_type='url')
    assert url == expected_url

    req = tc.get_agent_by_agent_name('test', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_projects():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/projects'
    url = tc.get_projects(return_type='url')
    assert url == expected_url

    req = tc.get_projects(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_projects_parent_project_id():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/projects'
    url = tc.get_projects(parent_project_id='foo', return_type='url')
    assert url == expected_url

    req = tc.get_projects(parent_project_id='foo', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_projects_mock_send():
    with mock.patch.object(tc.session, 'send') as mock_send:
        expected_data = {
            'count': 2,
            'href': '/httpAuth/app/rest/projects',
            'project': [
             {'description': 'Contains all other projects',
              'href': '/httpAuth/app/rest/projects/id:_Root',
              'id': '_Root',
              'name': '<Root project>',
              'webUrl': 'http://tcserver/project.html?projectId=_Root'},
             {'href': '/httpAuth/app/rest/projects/id:Admintools',
              'id': 'Admintools',
              'name': 'admintools',
              'parentProjectId': '_Root',
              'webUrl': 'http://tcserver/project.html?projectId=Admintools'},
            ]}
        mock_send.return_value = make_response(200, expected_data)
        projects = tc.get_projects()
        assert projects == expected_data


def test_get_projects_parent_project_id_mock_send():
    with mock.patch.object(tc.session, 'send') as mock_send:
        expected_data = {
            'count': 2,
            'href': '/httpAuth/app/rest/projects',
            'project': [
             {'description': 'Contains all other projects',
              'href': '/httpAuth/app/rest/projects/id:_Root',
              'id': '_Root',
              'name': '<Root project>',
              'webUrl': 'http://tcserver/project.html?projectId=_Root'},
             {'href': '/httpAuth/app/rest/projects/id:Admintools',
              'id': 'Admintools',
              'name': 'admintools',
              'parentProjectId': '_Root',
              'webUrl': 'http://tcserver/project.html?projectId=Admintools'},
             {'href': '/httpAuth/app/rest/projects/id:foo',
              'id': 'foo',
              'name': 'foo',
              'parentProjectId': '_Root',
              'webUrl': 'http://tcserver/project.html?projectId=foo'},
             {'href': '/httpAuth/app/rest/projects/id:foo_child',
              'id': 'foo_child',
              'name': 'foo_child',
              'parentProjectId': 'foo',
              'webUrl': 'http://tcserver/project.html?projectId=foo_child'},
            ]}
        mock_send.return_value = make_response(200, expected_data)
        data = tc.get_projects(parent_project_id='foo')
        assert data['count'] == 1
        projects = data['project']
        assert len(projects) == 1
        project = projects[0]
        assert project['id'] == 'foo_child'
        assert project['name'] == 'foo_child'
        assert project['parentProjectId'] == 'foo'


def test_get_project_by_project_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/projects/id:foo_project')
    url = tc.get_project_by_project_id('foo_project', return_type='url')
    assert url == expected_url

    req = tc.get_project_by_project_id('foo_project', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_project_by_project_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'projects/id:foo_project')
    url = tc.get_project_by_project_id(
        project_id='foo_project', return_type='url')
    assert url == expected_url

    req = tc.get_project_by_project_id(
        project_id='foo_project', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_server_info():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/server'
    url = tc.get_server_info(return_type='url')
    assert url == expected_url

    req = tc.get_server_info(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_plugins():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'server/plugins')
    url = tc.get_all_plugins(return_type='url')
    assert url == expected_url

    req = tc.get_all_plugins(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def make_response(status_code, data):
    response = requests.Response()
    response.headers['Content-Type'] = 'application/json'
    response.status_code = status_code
    response._content = json.dumps(data).encode('utf-8')
    return response


def test_get_builds_mock_send():
    with mock.patch.object(tc.session, 'send') as mock_send:
        expected_data = {
            "count": 1,
            "href": "/httpAuth/app/rest/builds/"
                    "?locator=branch:&start=0&count=100",
            'build': [
                {
                    "status": "FAILURE",
                    "defaultBranch": True,
                    "webUrl": "http://TEAMCITY_HOST:4567/viewLog.html"
                              "?buildId=70322&buildTypeId=Ansvc_Branches_Py34",
                    "number": "1",
                    "state": "finished",
                    "href": "/httpAuth/app/rest/builds/id:70322",
                    "branchName": "develop",
                    "buildTypeId": "Ansvc_Branches_Py34",
                    "id": 70322,
                },
            ]
        }
        mock_send.return_value = make_response(200, expected_data)
        data = tc.get_builds()
        assert data == expected_data


def test_get_builds_mock_send_simulate_error():
    with mock.patch.object(tc.session, 'send') as mock_send:
        expected_data = "Something's always wrong"
        mock_send.return_value = make_response(500, None)
        mock_send.return_value._content = expected_data.encode('utf-8')
        with pytest.raises(HTTPError) as excinfo:
            tc.get_builds()
        assert excinfo.value.status_code == 500
        assert str(excinfo.value) == expected_data


def test_get_builds_no_args():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?start=0&count=100')
    url = tc.get_builds(return_type='url')
    assert url == expected_url

    req = tc.get_builds(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_with_branch():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=branch:master'
                    '&start=0&count=100')
    url = tc.get_builds(branch='master', return_type='url')
    assert url == expected_url

    req = tc.get_builds(branch='master', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_with_start_and_count():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?start=0&count=3')
    url = tc.get_builds(start=0, count=3, return_type='url')
    assert url == expected_url

    req = tc.get_builds(start=0, count=3, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_with_start_and_count_and_branch():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=branch:master'
                    '&start=0&count=3')
    url = tc.get_builds(branch='master', start=0, count=3,
                        return_type='url')
    assert url == expected_url

    req = tc.get_builds(branch='master', start=0, count=3,
                        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_build_type():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=buildType:package'
                    '&start=0&count=100')
    url = tc.get_builds(
        build_type_id='package',
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        build_type_id='package',
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_build_type_and_branch_and_start_and_count():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=branch:master,buildType:package'
                    '&start=0&count=3')
    url = tc.get_builds(
        build_type_id='package', branch='master',
        start=0, count=3,
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        build_type_id='package', branch='master',
        start=0, count=3,
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_build_type_and_branch_and_status_start_and_count():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=branch:master,buildType:package,status:failure'
                    '&start=0&count=3')
    url = tc.get_builds(
        build_type_id='package', branch='master', status='failure',
        start=0, count=3,
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        build_type_id='package', branch='master', status='failure',
        start=0, count=3,
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_build_type_and_branch_and_tags_start_and_count():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=branch:master,buildType:package,tags:jobsvc'
                    '&start=0&count=3')
    url = tc.get_builds(
        build_type_id='package', branch='master', tags='jobsvc',
        start=0, count=3,
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        build_type_id='package', branch='master', tags='jobsvc',
        start=0, count=3,
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_build_type_and_branch_and_user_start_and_count():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=branch:master,buildType:package,user:johna'
                    '&start=0&count=3')
    url = tc.get_builds(
        build_type_id='package', branch='master', user='johna',
        start=0, count=3,
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        build_type_id='package', branch='master', user='johna',
        start=0, count=3,
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_build_type_and_start_and_count():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=buildType:package'
                    '&start=0&count=3')
    url = tc.get_builds(
        build_type_id='package',
        start=0, count=3,
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        build_type_id='package',
        start=0, count=3,
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url

def test_get_builds_by_since_build():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=sinceBuild:sinceTestBuild'
                    '&start=0&count=100')
    url = tc.get_builds(
        since_build='sinceTestBuild',
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        since_build='sinceTestBuild',
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url

def test_get_builds_by_until_build():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=untilBuild:untilTestBuild'
                    '&start=0&count=100')
    url = tc.get_builds(
        until_build='untilTestBuild',
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        until_build='untilTestBuild',
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url

def test_get_builds_by_since_date():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=sinceDate:sinceTestDate'
                    '&start=0&count=100')
    url = tc.get_builds(
        since_date='sinceTestDate',
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        since_date='sinceTestDate',
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_until_date():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=untilDate:untilTestDate'
                    '&start=0&count=100')
    url = tc.get_builds(
        until_date='untilTestDate',
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        until_date='untilTestDate',
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_builds_by_pinned():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/'
                    '?locator=pinned:True'
                    '&start=0&count=100')
    url = tc.get_builds(
        pinned=True,
        return_type='url')
    assert url == expected_url

    req = tc.get_builds(
        pinned=True,
        return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_by_build_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build')
    url = tc.get_build_by_build_id('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_by_build_id('foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_by_build_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build')
    url = tc.get_build_by_build_id(
        build_id='foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_by_build_id(
        build_id='foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_statistics_by_build_statistics_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build/statistics')
    url = tc.get_build_statistics_by_build_id(
        'foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_statistics_by_build_id(
        'foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_statistics_by_build_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build/statistics')
    url = tc.get_build_statistics_by_build_id(
        build_id='foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_statistics_by_build_id(
        build_id='foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_tags_by_build_tags_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build/tags')
    url = tc.get_build_tags_by_build_id('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_tags_by_build_id('foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_tags_by_build_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build/tags')
    url = tc.get_build_tags_by_build_id(
        build_id='foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_tags_by_build_id(
        build_id='foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_changes():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes?start=0&count=10')
    url = tc.get_all_changes(return_type='url')
    assert url == expected_url

    req = tc.get_all_changes(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_change_by_change_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/id:16884')
    url = tc.get_change_by_change_id(16884, return_type='url')
    assert url == expected_url

    req = tc.get_change_by_change_id(16884, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_change_by_change_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/id:16884')
    url = tc.get_change_by_change_id(change_id=16884, return_type='url')
    assert url == expected_url

    req = tc.get_change_by_change_id(change_id=16884, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_changes_by_build_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/build:id:73450')
    url = tc.get_changes_by_build_id(73450, return_type='url')
    assert url == expected_url

    req = tc.get_changes_by_build_id(73450, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_changes_by_build_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/build:id:73450')
    url = tc.get_changes_by_build_id(build_id=73450, return_type='url')
    assert url == expected_url

    req = tc.get_changes_by_build_id(build_id=73450, return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_types():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/buildTypes/'
    url = tc.get_build_types(return_type='url')
    assert url == expected_url

    req = tc.get_build_types(return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_type_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'buildTypes/id:foo_build')
    url = tc.get_build_type('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_type('foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_type_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'buildTypes/id:foo_build')
    url = tc.get_build_type(
        build_type_id='foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_type(
        build_type_id='foo_build', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_test():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'testOccurrences?locator=test:12345')

    url = tc.get_test(
        test_locator='12345', return_type='url')
    assert url == expected_url

    req = tc.get_test(
        test_locator='12345', return_type='request')
    assert req.method == 'GET'
    assert req.url == expected_url
