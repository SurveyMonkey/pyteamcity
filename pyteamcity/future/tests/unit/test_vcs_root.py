import responses

from pyteamcity.future import TeamCity

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
        "project": {
            "id": "_Root",
            "name": "<Root project>",
            "description": "Contains all other projects",
            "href": "/httpAuth/app/rest/projects/id:_Root",
            "properties": {
                "count": 13,
                "property": [
                    {
                        "name": "agentCleanFilesPolicy",
                        "value": "ALL_UNTRACKED",
                    },
                    {
                        "name": "agentCleanPolicy",
                        "value": "ALWAYS",
                    },
                    {
                        "name": "authMethod",
                        "value": "PASSWORD",
                    },
                    {
                        "name": "branch",
                        "value": "%sm.repo.default_branch%",
                    },
                    {
                        "name": "ignoreKnownHosts",
                        "value": "true",
                    },
                    {
                        "name": "secure:password",
                    },
                    {
                        "name": "submoduleCheckout",
                        "value": "CHECKOUT",
                    },
                    {
                        "name": "teamcity:branchSpec",
                        "value": "+:master\\n+:<default>\\n+:refs/heads/(<default>)\\n+:refs/heads/(*)\\n+:refs/pull/(*/merge)",  # noqa: E501
                    },
                    {
                        "name": "url",
                        "value": "https://github.com/SurveyMonkey/pyteamcity.git",  # noqa: E501
                    },
                    {
                        "name": "useAlternates",
                        "value": "true",
                    },
                    {
                        "name": "userForTags",
                        "value": "teamcity",
                    },
                    {
                        "name": "username",
                        "value": "teamcity",
                    },
                    {
                        "name": "usernameStyle",
                        "value": "USERID",
                    },
                ],
            },
            "vcsRootInstances": {
                "href": "/httpAuth/app/rest/vcs-root-instances?locator=vcsRoot:(id:CodeRepo)",  # noqa: E501
            },
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
