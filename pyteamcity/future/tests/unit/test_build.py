import datetime

from pyteamcity.future import TeamCity

tc = TeamCity.from_environ()


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


def test_unit_filter_by_build_type():
    builds = tc.builds.all().filter(
        build_type='DevOps_Metacloud_DeleteOldVMs',
        count=3)
    query_string = '?locator=buildType:DevOps_Metacloud_DeleteOldVMs'
    assert query_string in builds._get_url()


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
