from _pyteamcity import v2

tc = v2.TeamCity.from_environ()


def test_unit_get_all_projects():
    projects = tc.projects.all()
    assert projects._get_url().endswith('/app/rest/projects/')


def test_unit_filter_by_id():
    projects = tc.projects.all().filter(id='Txtasvc_Branches')
    assert projects._get_url().endswith(
        '/projects/?locator=id:Txtasvc_Branches')


def test_unit_filter_by_name():
    projects = tc.projects.all().filter(name='branches')
    assert projects._get_url().endswith(
        '/projects/?locator=name:branches')


def test_unit_get_by_id():
    url = tc.projects.all().get(id='Txtasvc_Branches', just_url=True)
    assert url.endswith('/projects/id:Txtasvc_Branches')
