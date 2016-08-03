from _pyteamcity import v2

tc = v2.TeamCity.from_environ()


def test_unit_get_all():
    users = tc.users.all()

    assert users._get_url().endswith('/app/rest/users/')


def test_unit_get_by_id():
    url = tc.users.all().get(id=16, just_url=True)
    assert url.endswith('/users/id:16')


def test_unit_get_by_username():
    url = tc.users.all().get(username='fred', just_url=True)
    assert url.endswith('/users/username:fred')
