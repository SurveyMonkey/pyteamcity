import requests

from teamcityrestapiclient import TeamCityRESTApiClient

user = 'TEAMCITY_USER'
password = 'TEAMCITY_PASSWORD'
host = 'TEAMCITY_HOST'
port = 4567

tc = TeamCityRESTApiClient(user, password, host, port)


def test_get_all_users():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/users'
    url = tc.get_all_users(return_type='url')
    assert url == expected_url

    req = tc.get_all_users(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_user_by_username():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'users/username:codyw')
    url = tc.get_user_by_username('codyw', return_type='url')
    assert url == expected_url

    req = tc.get_user_by_username('codyw', return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_vcs_roots():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/vcs-roots'
    url = tc.get_all_vcs_roots(return_type='url')
    assert url == expected_url

    req = tc.get_all_vcs_roots(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_vcs_root_by_vcs_root_id():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/vcs-roots/id:41'
    url = tc.get_vcs_root_by_vcs_root_id(41, return_type='url')
    assert url == expected_url

    req = tc.get_vcs_root_by_vcs_root_id(41, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_agents():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/agents'
    url = tc.get_agents(return_type='url')
    assert url == expected_url

    req = tc.get_agents(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_agent_by_agent_id():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/agents/id:41'
    url = tc.get_agent_by_agent_id(41, return_type='url')
    assert url == expected_url

    req = tc.get_agent_by_agent_id(41, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_projects():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/projects'
    url = tc.get_all_projects(return_type='url')
    assert url == expected_url

    req = tc.get_all_projects(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_project_by_project_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/projects/id:foo_project')
    url = tc.get_project_by_project_id('foo_project', return_type='url')
    assert url == expected_url

    req = tc.get_project_by_project_id('foo_project', return_type='request')
    assert isinstance(req, requests.PreparedRequest)
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
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_server_info():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/server'
    url = tc.get_server_info(return_type='url')
    assert url == expected_url

    req = tc.get_server_info(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_plugins():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'server/plugins')
    url = tc.get_all_plugins(return_type='url')
    assert url == expected_url

    req = tc.get_all_plugins(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_builds():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'builds/?start=0&count=3')
    url = tc.get_all_builds(start=0, count=3, return_type='url')
    assert url == expected_url

    req = tc.get_all_builds(start=0, count=3, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_builds_by_build_type_id():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'buildTypes/id:package/builds/?start=0&count=3')
    url = tc.get_all_builds_by_build_type_id(
        build_type_id='package', start=0, count=3, return_type='url')
    assert url == expected_url

    req = tc.get_all_builds_by_build_type_id(
        build_type_id='package', start=0, count=3, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_by_build_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build')
    url = tc.get_build_by_build_id('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_by_build_id('foo_build', return_type='request')
    assert isinstance(req, requests.PreparedRequest)
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
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_statistics_by_build_statistics_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build/statistics')
    url = tc.get_build_statistics_by_build_id('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_statistics_by_build_id('foo_build', return_type='request')
    assert isinstance(req, requests.PreparedRequest)
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
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_tags_by_build_tags_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest'
                    '/builds/id:foo_build/tags')
    url = tc.get_build_tags_by_build_id('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_tags_by_build_id('foo_build', return_type='request')
    assert isinstance(req, requests.PreparedRequest)
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
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_changes():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/changes'
    url = tc.get_all_changes(return_type='url')
    assert url == expected_url

    req = tc.get_all_changes(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_change_by_change_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/id:16884')
    url = tc.get_change_by_change_id(16884, return_type='url')
    assert url == expected_url

    req = tc.get_change_by_change_id(16884, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_change_by_change_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/id:16884')
    url = tc.get_change_by_change_id(change_id=16884, return_type='url')
    assert url == expected_url

    req = tc.get_change_by_change_id(change_id=16884, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_changes_by_build_id_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/build:id:73450')
    url = tc.get_changes_by_build_id(73450, return_type='url')
    assert url == expected_url

    req = tc.get_changes_by_build_id(73450, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_changes_by_build_id_kwarg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'changes/build:id:73450')
    url = tc.get_changes_by_build_id(build_id=73450, return_type='url')
    assert url == expected_url

    req = tc.get_changes_by_build_id(build_id=73450, return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_all_build_types():
    expected_url = 'http://TEAMCITY_HOST:4567/httpAuth/app/rest/buildTypes'
    url = tc.get_all_build_types(return_type='url')
    assert url == expected_url

    req = tc.get_all_build_types(return_type='request')
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url


def test_get_build_type_arg():
    expected_url = ('http://TEAMCITY_HOST:4567/httpAuth/app/rest/'
                    'buildTypes/id:foo_build')
    url = tc.get_build_type('foo_build', return_type='url')
    assert url == expected_url

    req = tc.get_build_type('foo_build', return_type='request')
    assert isinstance(req, requests.PreparedRequest)
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
    assert isinstance(req, requests.PreparedRequest)
    assert req.method == 'GET'
    assert req.url == expected_url
