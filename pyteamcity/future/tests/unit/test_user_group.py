from pyteamcity.future import TeamCity

tc = TeamCity.from_environ()


def test_unit_get_all():
    user_groups = tc.user_groups.all()
    assert user_groups._get_url().endswith('/app/rest/userGroups/')


def test_unit_get_by_key():
    url = tc.user_groups.all().get(key='SRE', just_url=True)
    assert url.endswith('/userGroups/key:SRE')
