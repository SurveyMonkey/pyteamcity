from _pyteamcity import v2

tc = v2.TeamCity.from_environ()


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
