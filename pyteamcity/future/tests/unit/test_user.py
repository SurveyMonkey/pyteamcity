import datetime

import responses

from pyteamcity.future import TeamCity

tc = TeamCity()


def test_unit_get_all():
    users = tc.users.all()

    assert users._get_url().endswith('/app/rest/users/')


def test_unit_get_by_id():
    url = tc.users.all().get(id=16, just_url=True)
    assert url.endswith('/users/id:16')


def test_unit_get_by_username():
    url = tc.users.all().get(username='fred', just_url=True)
    assert url.endswith('/users/username:fred')


@responses.activate
def test_unit_get_by_username_with_responses():
    last_login_string = '20160811T215944-0700'
    response_json = {
        'username': 'marca',
        'id': 16,
        'name': 'Marc Abramowitz',
        'lastLogin': last_login_string,
        'groups': {
            'count': 3,
            'group': [
                {
                    'name': 'All Users',
                    'key': 'ALL_USERS_GROUP',
                    'description': 'Contains all TeamCity users',
                },
                {
                    'name': 'DevOps',
                    'key': 'DEVOPS',
                    'description': 'DevOps Extended Team',
                },
                {
                    'name': 'TeamCity Admins',
                    'key': 'TEAMCITY_ADMINS',
                    'description': 'Administrators',
                },
            ],
        },
    }
    response_list_json = {
        'count': 1,
        'user': [response_json],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/users/'),
        json=response_list_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/users/username:marca'),
        json=response_json, status=200,
        content_type='application/json',
    )

    users = tc.users.all().filter(username='marca')
    assert len(users) == 1
    for user in users:
        assert user.username == 'marca'
    user = tc.users.all().get(username='marca')
    assert 'id=16' in repr(user)
    assert 'marca' in repr(user)
    assert 'Marc Abramowitz' in repr(user)
    assert isinstance(user.last_login_date, datetime.datetime)
    assert user.last_login_string == last_login_string
    assert user.last_login_date.year == 2016
    assert user.last_login_date.month == 8
    assert user.last_login_date.day == 11
    assert user.last_login_date.hour == 21
    assert user.last_login_date.minute == 59
    assert user.last_login_date.second == 44
    assert len(user.groups) == 3
    assert user.groups[0].name == 'All Users'
    assert user.groups[0].description == 'Contains all TeamCity users'
    assert user.groups[1].name == 'DevOps'
    assert user.groups[1].description == 'DevOps Extended Team'
    assert user.groups[2].name == 'TeamCity Admins'
    assert user.groups[2].description == 'Administrators'
