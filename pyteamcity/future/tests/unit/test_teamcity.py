import datetime

import pytest
import responses

from pyteamcity.future import exceptions, TeamCity


def test_username_and_password():
    tc = TeamCity(username='username', password='password')
    assert tc.base_url == 'http://127.0.0.1/httpAuth'
    assert tc.auth == ('username', 'password')


def test_non_standard_http_port():
    tc = TeamCity(protocol='http', port=8000)
    assert tc.base_url == 'http://127.0.0.1:8000/guestAuth'


def test_non_standard_https_port():
    tc = TeamCity(protocol='https', port=8000)
    assert tc.base_url == 'https://127.0.0.1:8000/guestAuth'


def test_from_environ(monkeypatch):
    monkeypatch.setenv('TEAMCITY_PROTO', 'https')
    monkeypatch.setenv('TEAMCITY_HOST', 'tcserver123')
    monkeypatch.setenv('TEAMCITY_USER', 'user123')
    monkeypatch.setenv('TEAMCITY_PASSWORD', 'password')
    tc = TeamCity.from_environ()
    assert tc.protocol == 'https'
    assert tc.server == 'tcserver123'
    assert tc.username == 'user123'
    assert tc.password == 'password'


@responses.activate
def test_unit_server_info_with_responses():
    tc = TeamCity()
    start_time_str = '20160811T130943-0700'
    current_time_str = '20160812T090424-0700'
    build_date_str = '20150918T000000-0700'
    response_json = {
        "version": "9.1.3 (build 37176)",
        "versionMajor": 9,
        "versionMinor": 1,
        "startTime": "20160811T130943-0700",
        "currentTime": "20160812T090424-0700",
        "buildNumber": "37176",
        "buildDate": "20150918T000000-0700",
        "internalId": "7a775607-5420-4a17-86a1-543d755d7210",
        "webUrl": "https://teamcity.company.com",
        "projects": {"href": "/httpAuth/app/rest/projects"},
        "vcsRoots": {"href": "/httpAuth/app/rest/vcs-roots"},
        "builds": {"href": "/httpAuth/app/rest/builds"},
        "users": {"href": "/httpAuth/app/rest/users"},
        "userGroups": {"href": "/httpAuth/app/rest/userGroups"},
        "agents": {"href": "/httpAuth/app/rest/agents"},
        "buildQueue": {"href": "/httpAuth/app/rest/buildQueue"},
        "agentPools": {"href": "/httpAuth/app/rest/agentPools"},
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/server'),
        json=response_json, status=200,
        content_type='application/json',
    )

    server_info = tc.server_info
    assert '9.1.3 (build 37176)' in repr(server_info)
    assert isinstance(server_info.start_time, datetime.datetime)
    assert server_info.start_time_str == start_time_str
    assert server_info.start_time.year == 2016
    assert server_info.start_time.month == 8
    assert server_info.start_time.day == 11
    assert server_info.start_time.hour == 13
    assert server_info.start_time.minute == 9
    assert server_info.start_time.second == 43
    assert isinstance(server_info.current_time, datetime.datetime)
    assert server_info.current_time_str == current_time_str
    assert server_info.current_time.year == 2016
    assert server_info.current_time.month == 8
    assert server_info.current_time.day == 12
    assert server_info.current_time.hour == 9
    assert server_info.current_time.minute == 4
    assert server_info.current_time.second == 24
    assert isinstance(server_info.build_date, datetime.datetime)
    assert server_info.build_date_str == build_date_str
    assert server_info.build_date.year == 2015
    assert server_info.build_date.month == 9
    assert server_info.build_date.day == 18


@responses.activate
def test_unit_server_info_exception_with_responses():
    tc = TeamCity()
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/server'),
        status=500,
    )

    with pytest.raises(exceptions.HTTPError):
        tc.server_info


@responses.activate
def test_unit_plugins_with_responses():
    tc = TeamCity()
    response_json = {
        'count': 97,
        'plugin': [
            {
                'version': '37176',
                'displayName': 'Agent System Info',
                'name': 'agent-system-info',
            },
            {
                'version': '37176',
                'displayName': 'Install Agent on remote host (agent push)',
                'name': 'agent.push',
            },
            {
                'version': '1.0.1',
                'displayName': 'Ansible Runner',
                'name': 'ansible-runner',
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/server/plugins'),
        json=response_json, status=200,
        content_type='application/json',
    )

    plugins = tc.plugins()
    assert plugins[0].name == 'agent-system-info'
    assert plugins[0].version == '37176'
    assert 'agent-system-info' in repr(plugins[0])
    assert plugins[1].name == 'agent.push'
    assert plugins[1].version == '37176'
    assert 'agent.push' in repr(plugins[1])
    assert plugins[2].name == 'ansible-runner'
    assert plugins[2].version == '1.0.1'
    assert 'ansible-runner' in repr(plugins[2])


@responses.activate
def test_unit_plugins_error():
    tc = TeamCity()
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/server/plugins'),
        status=500,
    )

    with pytest.raises(exceptions.HTTPError):
        tc.plugins()
