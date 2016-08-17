import pytest
import responses

from pyteamcity.future import exceptions, TeamCity

tc = TeamCity()


def test_unit_get_all():
    build_types = tc.build_types.all()
    assert build_types._get_url().endswith('/app/rest/buildTypes/')


def test_unit_filter_by_name():
    build_types = tc.build_types.all().filter(name='py27')
    assert build_types._get_url().endswith('/?locator=name:py27')


def test_unit_filter_by_project_id():
    build_types = tc.build_types.all().filter(
        project_id='Txtasvc_Branches')
    assert build_types._get_url().endswith(
        '/?locator=project:(id:Txtasvc_Branches)')


def test_unit_filter_by_affected_project_id():
    build_types = tc.build_types.all().filter(
        affected_project_id='Txtasvc')
    assert build_types._get_url().endswith(
        '/?locator=affectedProject:(id:Txtasvc)')


def test_unit_filter_by_template_flag():
    build_types = tc.build_types.all().filter(template_flag=True)
    assert build_types._get_url().endswith(
        '/?locator=templateFlag:True')


def test_unit_filter_by_paused():
    build_types = tc.build_types.all().filter(paused=True)
    assert build_types._get_url().endswith(
        '/?locator=paused:True')


def test_unit_filter_by_id():
    build_types = tc.build_types.all().filter(
        id='Txtasvc_Branches_Py27')
    assert build_types._get_url().endswith(
        '/?locator=id:Txtasvc_Branches_Py27')


def test_unit_get_by_id():
    url = tc.build_types.all().get(
        id='Txtasvc_Branches_Py27',
        just_url=True)
    assert url.endswith('/buildTypes/id:Txtasvc_Branches_Py27')


def _get_build_type_json():
    expected_raw_value = "".join([
        "password ",
        "display='hidden' ",
        "label='ansible_vault_password'",
    ])
    return {
        "id": "Txtasvc_Branches_Py27",
        "name": "py27",
        "projectName": "txtasvc :: branches",
        "projectId": "Txtasvc_Branches",
        "href": "/guestAuth/app/rest/buildTypes/id:Txtasvc_Branches_Py27",
        "project": {
            "id": "Txtasvc_Branches",
            "name": "branches",
            "parentProjectId": "Txtasvc",
        },
        "parameters": {
            "count": 3,
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


def _url_for_build_type(id):
    return tc.relative_url(
        'app/rest/buildTypes/id:{id}'.format(id=id)
    )


@responses.activate
def test_unit_get_by_id_with_responses():
    responses.add(
        responses.GET,
        _url_for_build_type('Txtasvc_Branches_Py27'),
        json=_get_build_type_json(), status=200,
        content_type='application/json',
    )
    project_json = {"id": "Txtasvc_Branches", "name": "branches"}
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/projects/id:Txtasvc_Branches'),
        json=project_json, status=200,
        content_type='application/json',
    )
    build_type = tc.build_types.all().get(id='Txtasvc_Branches_Py27')
    assert build_type.id == 'Txtasvc_Branches_Py27'
    assert 'Txtasvc_Branches_Py27' in repr(build_type)
    assert build_type.project.id == 'Txtasvc_Branches'
    params = build_type.parameters_dict
    assert params['env.PIP_USE_WHEEL'].value == 'true'
    assert 'Parameter' in repr(params['env.PIP_USE_WHEEL'])
    assert 'ptype=None' in repr(params['env.PIP_USE_WHEEL'])
    assert params['env.PIP_WHEEL_DIR'].value == '/tmp/wheelhouse'


@responses.activate
def test_unit_filter_by_template_id_with_responses():
    response_json = {
        "count": 3,
        "href": "/httpAuth/app/rest/buildTypes"
                "/?locator=template:(id:RunPipelineScript)",
        "buildType": [
            {
                "id": "Smform_Branches_Py27",
                "name": "py27",
                "projectName": "smform :: branches",
                "projectId": "Smform_Branches",
            },
            {
                "id": "Paymentgateway_ReleasePackage",
                "name": "release package",
                "projectName": "paymentgateway",
                "projectId": "Paymentgateway",
            },
            {
                "id": "Paymentgateway_PullRequests_Py27",
                "name": "py27",
                "projectName": "paymentgateway :: pull requests",
                "projectId": "Paymentgateway_PullRequests",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/buildTypes/'),
        json=response_json, status=200,
        content_type='application/json',
    )
    build_types = tc.build_types.all().filter(
        template_id='RunPipelineScript'
    )
    assert len(build_types) == 3
    for build_type in build_types:
        assert hasattr(build_type, 'name')


@responses.activate
def test_unit_set_paused():
    responses.add(
        responses.GET,
        _url_for_build_type('Txtasvc_Branches_Py27'),
        json=_get_build_type_json(), status=200,
        content_type='application/json',
    )
    build_type = tc.build_types.all().get(id='Txtasvc_Branches_Py27')

    # Try to set build_type as paused; it fails
    responses.add(
        responses.PUT,
        _url_for_build_type('Txtasvc_Branches_Py27') + '/paused',
        status=500,
    )
    with pytest.raises(exceptions.HTTPError):
        build_type.set_paused(True)


@responses.activate
def test_unit_reset_build_counter():
    responses.add(
        responses.GET,
        _url_for_build_type('Txtasvc_Branches_Py27'),
        json=_get_build_type_json(), status=200,
        content_type='application/json',
    )
    build_type = tc.build_types.all().get(id='Txtasvc_Branches_Py27')

    # Try to set build_type as paused; it fails
    responses.add(
        responses.PUT,
        _url_for_build_type('Txtasvc_Branches_Py27') +
        '/settings/buildNumberCounter',
        status=500,
    )
    with pytest.raises(exceptions.HTTPError):
        build_type.reset_build_counter(0)


@responses.activate
def test_unit_delete():
    responses.add(
        responses.GET,
        _url_for_build_type('Txtasvc_Branches_Py27'),
        json=_get_build_type_json(), status=200,
        content_type='application/json',
    )
    build_type = tc.build_types.all().get(id='Txtasvc_Branches_Py27')

    # Try to set build_type as paused; it fails
    responses.add(
        responses.DELETE,
        _url_for_build_type('Txtasvc_Branches_Py27'),
        status=500,
    )
    with pytest.raises(exceptions.HTTPError):
        build_type.delete()
