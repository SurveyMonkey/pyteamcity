import datetime

import pytest
import responses

from pyteamcity.future import exceptions, TeamCity

tc = TeamCity(username='user', password='password')


@responses.activate
def test_pin():
    response_json = {
        "id": 1467264,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "141",
        "href": "/httpAuth/app/rest/builds/id:1467264",
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.PUT,
        tc.relative_url('app/rest/builds/id:1467264/pin'),
        status=204,
    )

    build = tc.builds.all().get(id=1467264)
    build.pin('marca testing pinning')

    assert len(responses.calls) == 2
    req1 = responses.calls[0].request
    assert req1.method == 'GET'
    assert req1.url == tc.relative_url('app/rest/builds/id:1467264')
    req2 = responses.calls[1].request
    assert req2.url == tc.relative_url('app/rest/builds/id:1467264/pin')
    assert req2.body == 'marca testing pinning'


@responses.activate
def test_pin_HTTPError():
    response_json = {
        "id": 1467264,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "141",
        "href": "/httpAuth/app/rest/builds/id:1467264",
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.PUT,
        tc.relative_url('app/rest/builds/id:1467264/pin'),
        status=500,
    )

    build = tc.builds.all().get(id=1467264)
    with pytest.raises(exceptions.HTTPError):
        build.pin('marca testing pinning')


@responses.activate
def test_unpin():
    response_json = {
        "id": 1467264,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "141",
        "href": "/httpAuth/app/rest/builds/id:1467264",
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.DELETE,
        tc.relative_url('app/rest/builds/id:1467264/pin'),
        status=204,
    )

    build = tc.builds.all().get(id=1467264)
    build.unpin()

    assert len(responses.calls) == 2
    req1 = responses.calls[0].request
    assert req1.method == 'GET'
    assert req1.url == tc.relative_url('app/rest/builds/id:1467264')
    req2 = responses.calls[1].request
    assert req2.url == tc.relative_url('app/rest/builds/id:1467264/pin')


@responses.activate
def test_unpin_HTTPError():
    response_json = {
        "id": 1467264,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "141",
        "href": "/httpAuth/app/rest/builds/id:1467264",
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.DELETE,
        tc.relative_url('app/rest/builds/id:1467264/pin'),
        status=500,
    )

    build = tc.builds.all().get(id=1467264)
    with pytest.raises(exceptions.HTTPError):
        build.unpin()


def test_unit_get_all():
    builds = tc.builds.all()

    assert builds._get_url().endswith('/app/rest/builds/')


def test_unit_filter_by_since_date_string():
    since_date_string = '20160726T170030+0400'
    builds = tc.builds.all().filter(
        since_date=since_date_string,
        count=3)

    assert '/app/rest/builds/' in builds._get_url()


def test_unit_filter_by_since_datetime_object():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    builds = tc.builds.all().filter(
        since_date=yesterday,
        count=3)

    assert '/app/rest/builds/' in builds._get_url()


def test_unit_filter_by_since_build():
    builds = tc.builds.all().filter(
        since_build='id:1421166',
        count=3)
    assert '/app/rest/builds/' in builds._get_url()
    assert 'sinceBuild:(id:1421166)' in builds._get_url()


@responses.activate
def test_unit_filter_by_since_build_with_responses():
    response_json = {
        'count': 3,
        'build': [
            {
                'status': 'SUCCESS',
                'number': '510',
                'state': 'finished',
                'href': '/httpAuth/app/rest/builds/id:1469354',
                'buildTypeId': 'Exportlib_Branches_Py34',
                'id': 1469354,
            },
            {
                'status': 'SUCCESS',
                'number': '514',
                'state': 'finished',
                'href': '/httpAuth/app/rest/builds/id:1469353',
                'buildTypeId': 'Exportlib_Branches_Flake8',
                'id': 1469353,
            },
            {
                'status': 'SUCCESS',
                'number': '1012',
                'state': 'finished',
                'href': '/httpAuth/app/rest/builds/id:1469315',
                'buildTypeId': 'Apptelligence_ReleaseToSjc_Deploy',
                'id': 1469315,
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/'),
        json=response_json, status=200,
        content_type='application/json',
    )

    builds = tc.builds.all().filter(
        since_build='id:1421166',
        count=3)
    assert '/app/rest/builds/' in builds._get_url()
    assert 'sinceBuild:(id:1421166)' in builds._get_url()
    assert len(builds) == 3


def test_unit_filter_by_user():
    builds = tc.builds.all().filter(
        user='username:fred',
        count=3)
    assert '/app/rest/builds/' in builds._get_url()
    assert 'user:(username:fred)' in builds._get_url()


def test_unit_filter_by_id():
    builds = tc.builds.all().filter(id=1424513)
    assert '?locator=id:1424513' in builds._get_url()


def test_unit_get_by_id():
    url = tc.builds.all().get(id=1424513, just_url=True)
    assert '/id:1424513' in url


def test_unit_start():
    builds = tc.builds.all().filter(start=5)
    assert 'start:5' in builds._get_url()


def test_unit_count():
    builds = tc.builds.all().filter(count=5)
    assert 'count:5' in builds._get_url()


def test_unit_lookup_limit():
    builds = tc.builds.all().filter(lookup_limit=5)
    assert 'lookupLimit:5' in builds._get_url()


def test_unit_filter_by_project():
    builds = tc.builds.all().filter(
        project='Dummysvc_ReleaseToMt1',
        count=5)
    assert '?locator=project:(Dummysvc_ReleaseToMt1)' in builds._get_url()
    assert 'count:5' in builds._get_url()

    builds = tc.builds.all().filter(
        project='Dummysvc',
        count=5)
    assert '?locator=project:(Dummysvc)' in builds._get_url()
    assert 'count:5' in builds._get_url()


def test_unit_filter_by_affected_project():
    builds = tc.builds.all().filter(
        affected_project='Dummysvc_ReleaseToMt1',
        count=5)
    query_string = '?locator=affectedProject:(Dummysvc_ReleaseToMt1)'
    assert query_string in builds._get_url()

    builds = tc.builds.all().filter(
        affected_project='Dummysvc',
        count=5)
    assert '?locator=affectedProject:(Dummysvc)' in builds._get_url()


@responses.activate
def test_unit_filter_by_build_type():
    response_json = {
        'id': 'DevOps_Metacloud_DeleteOldVMs',
        'project': 'DevOps :: Metacloud',
    }
    uri = 'app/rest/buildTypes/id:DevOps_Metacloud_DeleteOldVMs'
    responses.add(
        responses.GET,
        tc.relative_url(uri),
        json=response_json, status=200,
        content_type='application/json',
    )
    response_json = {
        'count': 3,
        'build': [
            {
                'status': 'SUCCESS',
                'defaultBranch': True,
                'number': '339',
                'state': 'finished',
                'href': '/httpAuth/app/rest/builds/id:1467764',
                'branchName': 'master',
                'buildTypeId': 'DevOps_Metacloud_DeleteOldVMs',
                'id': 1467764,
            },
            {
                'status': 'SUCCESS',
                'defaultBranch': True,
                'number': '338',
                'state': 'finished',
                'href': '/httpAuth/app/rest/builds/id:1464784',
                'branchName': 'master',
                'buildTypeId': 'DevOps_Metacloud_DeleteOldVMs',
                'id': 1464784,
            },
            {
                'status': 'SUCCESS',
                'defaultBranch': True,
                'number': '337',
                'state': 'finished',
                'href': '/httpAuth/app/rest/builds/id:1460735',
                'branchName': 'master',
                'buildTypeId': 'DevOps_Metacloud_DeleteOldVMs',
                'id': 1460735,
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/'),
        json=response_json, status=200,
        content_type='application/json',
    )
    builds = tc.builds.all().filter(
        build_type='DevOps_Metacloud_DeleteOldVMs',
        count=3)
    query_string = '?locator=buildType:DevOps_Metacloud_DeleteOldVMs'
    assert query_string in builds._get_url()
    for build in builds:
        assert build.build_type.id == 'DevOps_Metacloud_DeleteOldVMs'


def test_unit_filter_by_number():
    builds = tc.builds.all().filter(number='332')
    assert '?locator=number:332' in builds._get_url()


def test_unit_filter_by_tags():
    builds = tc.builds.all().filter(
        build_type='Dummysvc_ReleaseToMt1_Deploy',
        tags='dummysvc_test_tag',
        count=3)
    assert 'tags:dummysvc_test_tag' in builds._get_url()
    assert 'buildType:Dummysvc_ReleaseToMt1_Deploy' in builds._get_url()


def test_unit_filter_by_tags_list():
    builds = tc.builds.all().filter(
        build_type='Dummysvc_ReleaseToMt1_Deploy',
        tags=['dummysvc_test_tag'])
    assert 'tags:dummysvc_test_tag' in builds._get_url()
    assert 'buildType:Dummysvc_ReleaseToMt1_Deploy' in builds._get_url()


def test_unit_filter_by_status_SUCCESS():
    builds = tc.builds.all().filter(
        build_type='Dummysvc_ReleaseToMt1_Deploy',
        status='SUCCESS')
    assert 'buildType:Dummysvc_ReleaseToMt1_Deploy' in builds._get_url()
    assert 'status:SUCCESS' in builds._get_url()


def test_unit_filter_by_status_FAILURE():
    builds = tc.builds.all().filter(
        build_type='Dummysvc_ReleaseToMt1_Deploy',
        status='FAILURE')
    assert 'buildType:Dummysvc_ReleaseToMt1_Deploy' in builds._get_url()
    assert 'status:FAILURE' in builds._get_url()


def test_unit_filter_by_personal():
    builds = tc.builds.all().filter(personal=True)
    assert '?locator=personal:True' in builds._get_url()


def test_unit_filter_by_canceled():
    builds = tc.builds.all().filter(canceled=True)
    assert '?locator=canceled:True' in builds._get_url()


def test_unit_filter_by_failed_to_start():
    builds = tc.builds.all().filter(failed_to_start=True)
    assert '?locator=failedToStart:True' in builds._get_url()


def test_unit_filter_by_running():
    builds = tc.builds.all().filter(running=True)
    assert '?locator=running:True' in builds._get_url()


def test_unit_filter_by_pinned():
    builds = tc.builds.all().filter(pinned=True)
    assert '?locator=pinned:True' in builds._get_url()


def test_unit_filter_by_agent_name():
    builds = tc.builds.all().filter(agent_name='tcagent112')
    assert '?locator=agentName:tcagent112' in builds._get_url()


def test_unit_filter_by_build_type_and_branch():
    builds = tc.builds.all().filter(
        build_type='DevOps_Metacloud_DeleteOldVMs',
        branch='master')
    assert 'buildType:DevOps_Metacloud_DeleteOldVMs' in builds._get_url()
    assert 'branch:master' in builds._get_url()


def test_unit_get_by_build_type_and_number():
    url = tc.builds.all().get(
        build_type='DevOps_Metacloud_DeleteOldVMs',
        number='332',
        just_url=True)
    assert '/buildType:DevOps_Metacloud_DeleteOldVMs,number:332' in url


@responses.activate
def test_parameters_dict_with_responses():
    response_json = {
        'id': 1467264,
        'buildTypeId': 'Dummysvc_Branches_Py27',
        'number': '141',
        'href': '/httpAuth/app/rest/builds/id:1467264',
        'properties': {
            'count': 1,
            'property': [
                {
                    'name': 'env.PYTHONWARNINGS',
                    'value': 'ignore',
                },
            ],
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=1467264)
    assert build.parameters_dict['env.PYTHONWARNINGS'].value == 'ignore'


@responses.activate
def test_api_url_with_responses():
    response_json = {'id': 1467264}
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=1467264)
    assert build.api_url.endswith('app/rest/builds/id:1467264')
