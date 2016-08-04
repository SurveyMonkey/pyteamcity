from pyteamcity.future import TeamCity

tc = TeamCity.from_environ()


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
    queued_builds = tc.queued_builds.all().filter(
        build_type=build_type)
    assert 'buildType:%s' % build_type in queued_builds._get_url()
