from pyteamcity.future import TeamCity

tc = TeamCity.from_environ()


def test_unit_get_all():
    vcs_roots = tc.vcs_roots.all()
    assert vcs_roots._get_url().endswith('/app/rest/vcs-roots/')


def test_unit_get_by_id():
    url = tc.vcs_roots.all().get(id=34, just_url=True)
    assert url.endswith('/vcs-roots/id:34')
