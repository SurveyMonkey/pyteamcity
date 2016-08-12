import datetime

import responses

from pyteamcity.future import TeamCity

tc = TeamCity()


def test_unit_all():
    queued_builds = tc.queued_builds.all()
    assert queued_builds._get_url().endswith('/app/rest/buildQueue/')


def test_unit_filter_by_project():
    queued_builds = tc.queued_builds.all().filter(
        project='Dummysvc_ReleaseToMt1',
        count=5)
    assert 'count:5' in queued_builds._get_url()
    assert 'project:(Dummysvc_ReleaseToMt1)' in queued_builds._get_url()


def test_unit_filter_by_build_type():
    build_type = 'DevOps_Metacloud_DeleteOldVMs'
    queued_builds = tc.queued_builds.all().filter(build_type=build_type)
    assert 'buildType:%s' % build_type in queued_builds._get_url()


@responses.activate
def test_unit_queued_build_with_responses():
    response_json = {
        "id": 1471658,
        "buildTypeId": "Responseweb_2_Branches_Package",
        "number": "2695",
        "status": "UNKNOWN",
        "state": "finished",
        "branchName": "preview",
        "href": "/httpAuth/app/rest/builds/id:1471658",
        "webUrl": "https://tcserver/viewLog.html"
                  "?buildId=1471658"
                  "&buildTypeId=Responseweb_2_Branches_Package",
        "statusText": "Canceled (Snapshot dependencies failed: 3 (new))",
        "buildType": {
            "id": "Responseweb_2_Branches_Package",
            "name": "package",
            "projectName": "responseweb :: branches",
            "projectId": "Responseweb_2_Branches",
            "href": "/httpAuth/app/rest/buildTypes"
                    "/id:Responseweb_2_Branches_Package",
            "webUrl": "https://tcserver/viewType.html"
                      "?buildTypeId=Responseweb_2_Branches_Package",
        },
        "canceledInfo": {
            "timestamp": "20160812T094513-0700",
            "text": "Build was canceled"
                    " because one of the builds it depends on failed",
        },
        "queuedDate": "20160812T094312-0700",
        "startDate": "20160812T094513-0700",
        "finishDate": "20160812T094513-0700",
    }
    response_list_json = {
        "count": 2,
        "href": "/httpAuth/app/rest/buildQueue/",
        "build": [
            {
                "id": 1455869,
                "buildTypeId": "Scansvc_PullRequests_Py27",
                "state": "queued",
                "branchName": "1/merge",
                "href": "/httpAuth/app/rest/buildQueue/id:1455869",
                "webUrl": "https://tcserver/viewQueued.html?itemId=1455869",
            },
            {
                "id": 1471658,
                "buildTypeId": "Responseweb_2_Branches_Package",
                "state": "queued",
                "branchName": "preview",
                "href": "/httpAuth/app/rest/buildQueue/id:1471658",
                "webUrl": "https://tcserver/viewQueued.html?itemId=1471658",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/buildQueue/'),
        json=response_list_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/buildQueue/id:1471658'),
        json=response_json, status=200,
        content_type='application/json',
    )

    queued_builds = tc.queued_builds.all()
    assert len(queued_builds) == 2
    for queued_build in queued_builds:
        assert hasattr(queued_build, 'build_type_id')
        assert hasattr(queued_build, 'branch_name')
        assert hasattr(queued_build, 'href')
        assert hasattr(queued_build, 'web_url')
    queued_build = tc.queued_builds.all().get(id=1471658)
    assert 'id=1471658' in repr(queued_build)
    assert 'Responseweb_2_Branches_Package' in repr(queued_build)
    assert isinstance(queued_build.queued_date, datetime.datetime)
    assert queued_build.queued_date.year == 2016
    assert queued_build.queued_date.month == 8
    assert queued_build.queued_date.day == 12
    assert queued_build.queued_date.hour == 9
    assert queued_build.queued_date.minute == 43
    assert queued_build.queued_date.second == 12
    assert queued_build.build_type.id == 'Responseweb_2_Branches_Package'
    assert queued_build.build_type.name == 'package'
