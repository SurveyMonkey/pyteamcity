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
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264/pin'),
        body='false', status=200,
        content_type='text/plain',
    )
    responses.add(
        responses.PUT,
        tc.relative_url('app/rest/builds/id:1467264/pin'),
        status=204,
        content_type='text/plain',
    )

    build = tc.builds.all().get(id=1467264)
    assert build.pinned is False
    build.pin('marca testing pinning')

    assert len(responses.calls) == 3

    req = responses.calls[0].request
    assert req.method == 'GET'
    assert req.url == tc.relative_url('app/rest/builds/id:1467264')

    req = responses.calls[1].request
    assert req.method == 'GET'
    assert req.url == tc.relative_url('app/rest/builds/id:1467264/pin')

    req = responses.calls[2].request
    assert req.url == tc.relative_url('app/rest/builds/id:1467264/pin')
    assert req.body == 'marca testing pinning'


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
    req1 = responses.calls[1].request
    assert req1.url == tc.relative_url('app/rest/builds/id:1467264/pin')


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
    expected_raw_value = "".join([
        "password ",
        "display='hidden' ",
        "label='ansible_vault_password'",
    ])
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
                {
                    'type': {
                        'rawValue': expected_raw_value,
                    },
                    'name': 'env.ANSIBLE_VAULT_PASSWORD',
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
    param = build.parameters_dict['env.ANSIBLE_VAULT_PASSWORD']
    assert param.ptype['rawValue'] == expected_raw_value


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


@responses.activate
def test_repr_with_responses():
    build_id = 1467264
    response_json = {
        'id': build_id,
        'buildTypeId': 'Dummysvc_Branches_Py27',
        'number': '141',
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:%d' % build_id),
        json=response_json, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=build_id)
    assert 'id=1467264' in repr(build)
    assert 'Dummysvc_Branches_Py27' in repr(build)
    assert '141' in repr(build)


@responses.activate
def test_user_with_responses():
    build_id = 1467264
    response_json = {
        'id': build_id,
        'triggered': {
            'date': '20160810T172739-0700',
            'type': 'user',
            'user': {
                'username': 'marca',
                'href': '/httpAuth/app/rest/users/id:16',
                'name': 'Marc Abramowitz',
                'id': 16,
            },
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:%d' % build_id),
        json=response_json, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=build_id)
    assert build.user.username == 'marca'
    assert build.user.id == 16


@responses.activate
def test_agent_with_responses():
    build_id = 1467264
    response_json = {
        'id': build_id,
        'agent': {
            'typeId': 57,
            'href': '/httpAuth/app/rest/agents/id:57',
            'id': 57,
            'name': 'tcagent111',
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:%d' % build_id),
        json=response_json, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=build_id)
    assert build.agent.name == 'tcagent111'
    assert build.agent.id == 57


@responses.activate
def test_dates_with_responses():
    build_id = 1467264
    queued_date_string = '20160810T172739-0700'
    start_date_string = '20160810T172741-0700'
    finish_date_string = '20160810T172802-0700'
    response_json = {
        'id': build_id,
        'queuedDate': queued_date_string,
        'startDate': start_date_string,
        'finishDate': finish_date_string,
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1467264'),
        json=response_json, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=build_id)
    assert isinstance(build.queued_date, datetime.datetime)
    assert build.queued_date_string == queued_date_string
    assert build.queued_date.year == 2016
    assert build.queued_date.month == 8
    assert build.queued_date.day == 10
    assert build.queued_date.hour == 17
    assert build.queued_date.minute == 27
    assert build.queued_date.second == 39
    assert isinstance(build.start_date, datetime.datetime)
    assert build.start_date_string == start_date_string
    assert build.start_date.year == 2016
    assert build.start_date.month == 8
    assert build.start_date.day == 10
    assert build.start_date.hour == 17
    assert build.start_date.minute == 27
    assert build.start_date.second == 41
    assert isinstance(build.finish_date, datetime.datetime)
    assert build.finish_date_string == finish_date_string
    assert build.finish_date.year == 2016
    assert build.finish_date.month == 8
    assert build.finish_date.day == 10
    assert build.finish_date.hour == 17
    assert build.finish_date.minute == 28
    assert build.finish_date.second == 2


def test_download_build_log():
    log_content_length = 100
    response_json = {
        "id": 1467264,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "141",
        "href": "/httpAuth/app/rest/builds/id:1467264",
    }

    resp_builds = {
        'method': responses.GET,
        'url': tc.relative_url('app/rest/builds/id:1467264'),
        'json': response_json,
        'status': 200,
        'content_type': 'application/json',
    }

    resp_buildlog = {
        'url': tc.relative_url('downloadBuildLog.html?buildId=1467264'),
        'body': 'a' * log_content_length,
        'status': 200,
        'match_querystring': True,
        'content_type': 'text/plain;charset=UTF-8',
        'adding_headers': {'content-length': str(log_content_length)},
    }

    resp_archived_buildlog = resp_buildlog.copy()
    resp_archived_buildlog['url'] += '&archived=true'

    with responses.RequestsMock() as resp:
        resp.add(**resp_builds)
        resp.add(**dict(method='GET',  **resp_buildlog))

        build = tc.builds.all().get(id=1467264)
        assert build.build_log == resp_buildlog['body']

    with responses.RequestsMock() as resp:
        resp.add(**resp_builds)
        resp.add(**dict(method='GET',  **resp_archived_buildlog))
        resp.add(**dict(method='HEAD', **resp_buildlog))
        resp.add(**dict(method='GET',  **resp_buildlog))
        resp.add(**dict(method='HEAD', **resp_buildlog))

        build = tc.builds.all().get(id=1467264)
        assert build.get_build_log(content_length=log_content_length) == resp_buildlog['body']
        assert build.get_build_log(archived=True) == resp_buildlog['body']

        with pytest.raises(exceptions.ArtifactSizeExceeded):
            build.get_build_log(content_length=log_content_length - 1)
