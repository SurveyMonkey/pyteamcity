import webbrowser

import pytest
import responses

from pyteamcity.future import exceptions, TeamCity

tc = TeamCity()


def test_unit_get_all_projects():
    projects = tc.projects.all()
    assert projects._get_url().endswith('/app/rest/projects/')


def test_unit_filter_by_id():
    projects = tc.projects.all().filter(id='Txtasvc_Branches')
    assert projects._get_url().endswith(
        '/projects/?locator=id:Txtasvc_Branches')


@responses.activate
def test_unit_create_project_with_responses():
    # Simulate failure creating a project
    responses.add(
        responses.POST,
        tc.relative_url('app/rest/projects/'),
        status=500, body='Internal error',
    )
    with pytest.raises(exceptions.HTTPError) as excinfo:
        tc.projects.all().create(name='foo')
    assert str(excinfo.value) == 'Internal error'

    # Simulate success creating a project
    response_json = {
        "name": "foo",
        "id": "foo101",
        "href": "/guestAuth/app/rest/projects/id:foo101",
    }
    responses.reset()
    responses.add(
        responses.POST,
        tc.relative_url('app/rest/projects/'),
        json=response_json, status=200,
        content_type='application/json',
    )
    project = tc.projects.all().create(name='foo', id='foo101')
    assert project.id == 'foo101'
    assert 'foo' in repr(project)

    # Now simulate failure creating a build type
    responses.add(
        responses.POST,
        tc.relative_url('app/rest/projects/id:foo101/buildTypes'),
        status=500,
    )
    with pytest.raises(exceptions.HTTPError):
        project.create_build_type('test')

    # Now simulate success creating a build type
    responses.reset()
    responses.add(
        responses.POST,
        tc.relative_url('app/rest/projects/id:foo101/buildTypes'),
        json={'id': 'test', 'name': 'test'}, status=200,
    )
    build_type = project.create_build_type('test')
    assert build_type.id == 'test'
    assert build_type.name == 'test'

    # Now test deleting the project
    responses.add(
        responses.DELETE,
        tc.relative_url('app/rest/projects/id:foo101'),
        status=500,
    )
    with pytest.raises(exceptions.HTTPError):
        project.delete()


@responses.activate
def test_unit_fetch_401_failure_with_responses():
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/'),
        status=401,
    )
    projects = tc.projects.all().filter(id='Txtasvc_Branches')
    with pytest.raises(exceptions.UnauthorizedError):
        assert len(projects) == 1


@responses.activate
def test_unit_fetch_500_failure_with_responses():
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/'),
        status=500,
    )
    projects = tc.projects.all().filter(id='Txtasvc_Branches')
    with pytest.raises(exceptions.HTTPError):
        assert len(projects) == 1


@responses.activate
def test_unit_filter_by_id_with_responses(monkeypatch):
    response_json = {
        "count": 1,
        "href": "/httpAuth/app/rest/projects/?locator=id:Txtasvc_Branches",
        "project": [
            {
                "id": "Txtasvc_Branches",
                "name": "branches",
                "parentProjectId": "Txtasvc",
                "href": "/httpAuth/app/rest/projects/id:Txtasvc_Branches",
                "webUrl": "https://tcserver/project.html"
                          "?projectId=Txtasvc_Branches",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/'),
        json=response_json, status=200,
        content_type='application/json',
    )
    projects = tc.projects.all().filter(id='Txtasvc_Branches')
    assert len(projects) == 1
    for project in projects:
        assert project.id == 'Txtasvc_Branches'
        assert 'Txtasvc_Branches' in repr(project)
        monkeypatch.setattr(webbrowser, 'open', lambda url: url)
        project.open_web_browser()


@responses.activate
def test_unit_get_by_id_with_responses():
    expected_raw_value = "".join([
        "password ",
        "display='hidden' ",
        "label='ansible_vault_password'",
    ])
    response_json = {
        "id": "Txtasvc_Branches",
        "name": "branches",
        "parentProjectId": "Txtasvc",
        "parentProject": {
            "id": "Txtasvc",
            "name": "txtasvc",
            "parentProjectId": "_Root",
        },
        "buildTypes": {
            "count": 3,
            "buildType": [
                {
                    "id": "Txtasvc_Branches_Package",
                    "name": "package",
                    "projectName": "txtasvc :: branches",
                    "projectId": "Txtasvc_Branches",
                },
                {
                    "id": "Txtasvc_Branches_Pep8",
                    "name": "pep8",
                    "projectName": "txtasvc :: branches",
                    "projectId": "Txtasvc_Branches",
                },
                {
                    "id": "Txtasvc_Branches_Py27",
                    "name": "py27",
                    "projectName": "txtasvc :: branches",
                    "projectId": "Txtasvc_Branches",
                },
            ],
        },
        "parameters": {
            "count": 2,
            "property": [
                {
                    "name": "env.PIP_USE_WHEEL",
                    "value": "true",
                },
                {
                    "name": "env.PIP_WHEEL_DIR",
                    "value": "/tmp/wheelhouse",
                },
                {
                    'name': 'env.ANSIBLE_VAULT_PASSWORD',
                    'type': {'rawValue': expected_raw_value},
                },
            ],
        },
    }
    response2_json = {
        "id": "Txtasvc",
        "name": "txtasvc",
        "parentProjectId": "_Root",
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/id:Txtasvc_Branches'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/id:Txtasvc'),
        json=response2_json, status=200,
        content_type='application/json',
    )
    project = tc.projects.all().get(id='Txtasvc_Branches')
    assert project.id == 'Txtasvc_Branches'
    assert 'Txtasvc_Branches' in repr(project)
    assert project.parent_project.id == 'Txtasvc'
    params = project.parameters_dict
    assert params['env.PIP_USE_WHEEL'].value == 'true'
    assert 'Parameter' in repr(params['env.PIP_USE_WHEEL'])
    assert 'ptype=None' in repr(params['env.PIP_USE_WHEEL'])
    assert params['env.PIP_WHEEL_DIR'].value == '/tmp/wheelhouse'


@responses.activate
def test_unit_subprojects():
    response_json = {
        "id": "Txtasvc",
        "name": "txtasvc",
        "parentProjectId": "_Root",
        "projects": {
            "count": 8,
            "project": [
                {
                    "id": "Txtasvc_Branches",
                    "name": "branches",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_PullRequests",
                    "name": "pull requests",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_ReleaseToMt1",
                    "name": "release to mt1",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_ReleaseToMt2",
                    "name": "release to mt2",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_ReleaseToMt3",
                    "name": "release to mt3",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_ReleaseToMt4",
                    "name": "release to mt4",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_ReleaseToMt5",
                    "name": "release to mt5",
                    "parentProjectId": "Txtasvc",
                },
                {
                    "id": "Txtasvc_ReleaseToSjc",
                    "name": "release to sjc",
                    "parentProjectId": "Txtasvc",
                },
            ],
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/id:Txtasvc'),
        json=response_json, status=200,
        content_type='application/json',
    )
    project = tc.projects.all().get(id='Txtasvc')
    assert project.id == 'Txtasvc'
    assert project.name == 'txtasvc'
    assert len(project.projects) == 8
    assert project.projects[4].id == 'Txtasvc_ReleaseToMt3'
    for p in project.projects:
        assert p.parent_project.id == 'Txtasvc'


@responses.activate
def test_unit_build_types():
    response_json = {
        "id": "Txtasvc_Branches",
        "name": "branches",
        "parentProjectId": "Txtasvc",
        "href": "/httpAuth/app/rest/projects/id:Txtasvc_Branches",
        "webUrl": "https://tcserver/project.html"
                  "?projectId=Txtasvc_Branches",
        "parentProject": {
            "id": "Txtasvc",
            "name": "txtasvc",
            "parentProjectId": "_Root",
            "href": "/httpAuth/app/rest/projects/id:Txtasvc",
            "webUrl": "https://tcserver/project.html?projectId=Txtasvc",
        },
        "buildTypes": {
            "count": 3,
            "buildType": [
                {
                    "id": "Txtasvc_Branches_Package",
                    "name": "package",
                    "projectName": "txtasvc :: branches",
                    "projectId": "Txtasvc_Branches",
                },
                {
                    "id": "Txtasvc_Branches_Pep8",
                    "name": "pep8",
                    "projectName": "txtasvc :: branches",
                    "projectId": "Txtasvc_Branches",
                },
                {
                    "id": "Txtasvc_Branches_Py27",
                    "name": "py27",
                    "projectName": "txtasvc :: branches",
                    "projectId": "Txtasvc_Branches",
                },
            ],
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/id:Txtasvc_Branches'),
        json=response_json, status=200,
        content_type='application/json',
    )
    project = tc.projects.all().get(id='Txtasvc_Branches')
    assert project.id == 'Txtasvc_Branches'
    assert project.name == 'branches'

    response_json = {
        "count": 3,
        "href": "/httpAuth/app/rest/buildTypes/"
                "?locator=project:(id:Txtasvc_Branches)",
        "buildType": [
            {
                "id": "Txtasvc_Branches_Package",
                "name": "package",
                "projectName": "txtasvc :: branches",
                "projectId": "Txtasvc_Branches",
            },
            {
                "id": "Txtasvc_Branches_Pep8",
                "name": "pep8",
                "projectName": "txtasvc :: branches",
                "projectId": "Txtasvc_Branches",
            },
            {
                "id": "Txtasvc_Branches_Py27",
                "name": "py27",
                "projectName": "txtasvc :: branches",
                "projectId": "Txtasvc_Branches",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/buildTypes/'),
        json=response_json, status=200,
        content_type='application/json',
    )
    assert len(project.build_types) == 3


def test_unit_filter_by_name():
    projects = tc.projects.all().filter(name='branches')
    assert projects._get_url().endswith(
        '/projects/?locator=name:branches')


def test_unit_get_by_id():
    url = tc.projects.all().get(id='Txtasvc_Branches', just_url=True)
    assert url.endswith('/projects/id:Txtasvc_Branches')
