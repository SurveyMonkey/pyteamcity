import pytest
import responses

from pyteamcity.future import exceptions, TeamCity

tc = TeamCity()


def test_unit_get_all():
    vcs_roots = tc.vcs_roots.all()
    assert vcs_roots._get_url().endswith('/app/rest/vcs-roots/')


def test_unit_get_by_id():
    url = tc.vcs_roots.all().get(id='CodeRepo', just_url=True)
    assert url.endswith('/vcs-roots/id:CodeRepo')


@responses.activate
def test_unit_get_with_responses():
    response_json = {
        "id": "CodeRepo",
        "name": "code repo",
        "vcsName": "jetbrains.git",
        "status": "FINISHED",
        "lastChecked": "20160812T075822-0700",
        "href": "/httpAuth/app/rest/vcs-roots/id:CodeRepo",
        "properties": {
            "count": 13,
            "property": [
                {"name": "agentCleanFilesPolicy",
                 "value": "ALL_UNTRACKED"},
                {"name": "agentCleanPolicy",
                 "value": "ALWAYS"},
                {"name": "authMethod",
                 "value": "PASSWORD"},
                {"name": "branch",
                 "value": "%sm.repo.default_branch%"},
                {"name": "ignoreKnownHosts",
                 "value": "true"},
                {"name": "secure:password"},
                {"name": "submoduleCheckout",
                 "value": "CHECKOUT"},
                {"name": "teamcity:branchSpec",
                 "value": "+:master\\n+:<default>\\n+:refs/heads/(<default>)\\n+:refs/heads/(*)\\n+:refs/pull/(*/merge)"},  # noqa: E501
                {"name": "url",
                 "value": "https://github.com/SurveyMonkey/pyteamcity.git"},  # noqa: E501
                {"name": "useAlternates",
                 "value": "true"},
                {"name": "userForTags",
                 "value": "teamcity"},
                {"name": "username",
                 "value": "teamcity"},
                {"name": "usernameStyle",
                 "value": "USERID"},
            ],
        },
        "vcsRootInstances": {
            "href": "/httpAuth/app/rest/vcs-root-instances?locator=vcsRoot:(id:CodeRepo)",  # noqa: E501
        },
        "project": {
            "id": "_Root",
            "name": "<Root project>",
            "description": "Contains all other projects",
            "href": "/httpAuth/app/rest/projects/id:_Root",
        },
    }
    response_list_json = {
        'count': 1,
        'vcs-root': [response_json],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/vcs-roots/'),
        json=response_list_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/vcs-roots/id:CodeRepo'),
        json=response_json, status=200,
        content_type='application/json',
    )

    vcs_roots = tc.vcs_roots.all().filter(name='code repo')
    assert len(vcs_roots) == 1
    vcs_roots = tc.vcs_roots.all().filter(id='CodeRepo')
    assert len(vcs_roots) == 1
    for vcs_root in vcs_roots:
        assert vcs_root.name == 'code repo'
    vcs_root = tc.vcs_roots.all().get(id='CodeRepo')
    assert 'code repo' in repr(vcs_root)
    assert 'CodeRepo' in repr(vcs_root)


@responses.activate
def test_unit_create_vcs_root_with_responses():
    vcs_url = 'https://github.com/SurveyMonkey/pyteamcity.git'

    # Simulate failure creating a VCSRoot
    responses.add(
        responses.POST,
        tc.relative_url('app/rest/vcs-roots/'),
        status=500, body='Internal error',
    )
    with pytest.raises(exceptions.HTTPError) as excinfo:
        tc.vcs_roots.all().create(
            name='pyteamcity',
            vcs_name='jetbrains.git',
            url=vcs_url,
            branch='master',
        )
    assert str(excinfo.value) == 'Internal error'

    # Simulate success creating a VCSRoot
    response_json = {
        'name': 'pyteamcity',
        'id': 'Root_Pyteamcity',
        'href': '/guestAuth/app/rest/vcs-roots/id:Root_Pyteamcity',
        'properties': {
            'property': [
                {'name': 'url', 'value': vcs_url},
                {'name': 'branch', 'value': 'master'},
                {"name": "teamcity:branchSpec",
                 "value": "+:master\n+:<default>\n+:refs/heads/(<default>)\n+:refs/heads/(*)\n+:refs/pull/(*/merge)"},  # noqa: E501
            ],
        },
    }
    responses.reset()
    responses.add(
        responses.POST,
        tc.relative_url('app/rest/vcs-roots/'),
        json=response_json, status=200,
        content_type='application/json',
    )
    branch_spec = '\n'.join([
        '+:master',
        '+:<default>',
        '+:refs/heads/(<default>)',
        '+:refs/heads/(*)',
        '+:refs/pull/(*/merge)',
    ])
    vcs_root = tc.vcs_roots.all().create(
        name='pyteamcity',
        vcs_name='jetbrains.git',
        url=vcs_url,
        branch='master',
        branch_spec=branch_spec,
        user_for_tags='tagman',
        username='bob',
        id='Root_Pyteamcity',
    )

    try:
        assert vcs_root.id == 'Root_Pyteamcity'
        assert 'pyteamcity' in repr(vcs_root)
        assert vcs_root.url == vcs_url
        assert vcs_root.branch == 'master'
        assert vcs_root.branch_spec == branch_spec
    finally:
        # Now test deleting the VCSRoot and it fails
        responses.add(
            responses.DELETE,
            tc.relative_url(
                'app/rest/vcs-roots/id:Root_Pyteamcity'),
            status=500,
        )
        with pytest.raises(exceptions.HTTPError):
            vcs_root.delete()

        # Now test deleting the VCSRoot and it succeeds
        responses.reset()
        responses.add(
            responses.DELETE,
            tc.relative_url(
                'app/rest/vcs-roots/id:Root_Pyteamcity'),
            status=200,
        )
        vcs_root.delete()
