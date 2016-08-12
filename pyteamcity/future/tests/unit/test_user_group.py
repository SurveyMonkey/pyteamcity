import responses

from pyteamcity.future import TeamCity

tc = TeamCity()


def test_unit_get_all():
    user_groups = tc.user_groups.all()
    assert user_groups._get_url().endswith('/app/rest/userGroups/')


def test_unit_get_by_key():
    url = tc.user_groups.all().get(key='SRE', just_url=True)
    assert url.endswith('/userGroups/key:SRE')


@responses.activate
def test_unit_get_with_responses():
    response_json = {
        "key": "SRE",
        "name": "SRE",
        "href": "/httpAuth/app/rest/userGroups/key:SRE",
        "description": "Site Reliability Engineering",
        "users": {
            "count": 1,
            "user": [
                {
                    "username": "josephz",
                    "name": "Joseph Z.",
                    "id": 168,
                    "href": "/httpAuth/app/rest/users/id:168",
                },
            ],
        },
        "properties": {
            "count": 0,
            "href": "/app/rest/userGroups/key:SRE/properties",
            "property": [],
        },
        "parent-groups": {
            "count": 0,
            "group": [],
        },
        "child-groups": {
            "count": 0,
            "group": [],
        },
        "roles": {
            "role": [
                {
                    "roleId": "PROJECT_ADMIN",
                    "scope": "p:_Root",
                },
            ],
        },
    }
    response_list_json = {
        'count': 1,
        'group': [
            {
                "key": "SRE",
                "name": "SRE",
                "href": "/httpAuth/app/rest/userGroups/key:SRE",
                "description": "Site Reliability Engineering",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/userGroups/'),
        json=response_list_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/userGroups/key:SRE'),
        json=response_json, status=200,
        content_type='application/json',
    )

    user_groups = tc.user_groups.all().filter(key='SRE')
    assert len(user_groups) == 1
    user_groups = tc.user_groups.all().filter(name='SRE')
    assert len(user_groups) == 1
    for user_group in user_groups:
        assert user_group.key == 'SRE'
    user_group = tc.user_groups.all().get(key='SRE')
    assert 'SRE' in repr(user_group)
    assert 'Site Reliability Engineering' in repr(user_group)
    assert len(user_group.users) == 1
    assert user_group.users[0].name == 'Joseph Z.'
