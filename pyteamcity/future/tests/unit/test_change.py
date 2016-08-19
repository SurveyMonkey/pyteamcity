import datetime

import responses

from pyteamcity.future import TeamCity

tc = TeamCity()


def test_unit_get_all():
    changes = tc.changes.all()
    assert changes._get_url().endswith('/app/rest/changes/')


def test_unit_get_by_id():
    url = tc.changes.all().get(id=276198, just_url=True)
    assert url.endswith('/changes/id:276198')


@responses.activate
def test_unit_get_by_id_with_responses():
    change_json = {
        'username': 'jonathana',
        'comment': 'removed marquee :(\n',
        'href': '/httpAuth/app/rest/changes/id:276197',
        'vcsRootInstance': {
            'id': '1636',
            'vcs-root-id': 'CodeRepo',
            'name': 'code repo',
        },
        'version': '2e5208d25c37da65c248967ecc53a37e48accba7',
        'user': {
            'username': 'jonathana',
            'href': '/httpAuth/app/rest/users/id:210',
            'name': 'Jonathan Allen',
            'id': 210,
        },
        'date': '20160614T112250-0700',
        'id': 276197,
        'files': {
            'file': [
                {
                    'relative-file': 'dummysvc/views/templates/hello.jinja2',
                    'file': 'dummysvc/views/templates/hello.jinja2',
                    'before-revision': 'f433142360c36d62f11ebb0d434ddfded394c5a5',  # noqa: E501
                    'after-revision': '2e5208d25c37da65c248967ecc53a37e48accba7',  # noqa: E501
                },
            ],
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/id:276197'),
        json=change_json, status=200,
        content_type='application/json',
    )

    change = tc.changes.all().get(id=276197)

    assert change.id == 276197
    assert change.version == '2e5208d25c37da65c248967ecc53a37e48accba7'
    assert change.username == 'jonathana'
    assert change.date.year == 2016
    assert change.date.month == 6
    assert change.date.day == 14
    assert change.date.hour == 11
    assert change.date.minute == 22
    assert change.date.second == 50
    assert str(change.id) in repr(change)
    assert change.version in repr(change)


@responses.activate
def test_filter_by_project():
    changes_json = {
        "count": 3,
        "change": [
            {
                "id": 276198,
                "version": "28f394a872c1cde701",
                "username": "jonathana",
                "date": "20160614T112304-0700",
            },
            {
                "id": 276197,
                "version": "2e5208d25c37da65c2",
                "username": "jonathana",
                "date": "20160614T112250-0700",
            },
            {
                "id": 276196,
                "version": "e5896e287850f52e8f",
                "username": "jinboz",
                "date": "20160614T112247-0700",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/'),
        json=changes_json, status=200,
        content_type='application/json',
    )

    changes = tc.changes.all().filter(
        project='Dummysvc_Branches',
        start=1,
        count=3,
        lookup_limit=20,
    )
    assert len(changes) == 3
    for change in changes:
        assert hasattr(change, 'id')
        assert hasattr(change, 'version')
        assert hasattr(change, 'username')
        assert isinstance(change.date, datetime.datetime)
        assert hasattr(change, 'href')
        assert hasattr(change, 'web_url')


@responses.activate
def test_filter_by_build_type():
    changes_json = {
        "count": 3,
        "change": [
            {
                "id": 276198,
                "version": "28f394a872c1cde701",
                "username": "jonathana",
                "date": "20160614T112304-0700",
            },
            {
                "id": 276197,
                "version": "2e5208d25c37da65c2",
                "username": "jonathana",
                "date": "20160614T112250-0700",
            },
            {
                "id": 276196,
                "version": "e5896e287850f52e8f",
                "username": "jinboz",
                "date": "20160614T112247-0700",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/'),
        json=changes_json, status=200,
        content_type='application/json',
    )

    changes = tc.changes.all().filter(
        build_type='Dummysvc_Branches_Py27',
        count=3,
    )
    assert len(changes) == 3
    for change in changes:
        assert hasattr(change, 'id')
        assert hasattr(change, 'version')
        assert hasattr(change, 'username')
        assert isinstance(change.date, datetime.datetime)
        assert hasattr(change, 'href')
        assert hasattr(change, 'web_url')


@responses.activate
def test_filter_by_build():
    changes_json = {
        'count': 2,
        'change': [
            {
                'username': 'bradd',
                'version': '124b46cb36a05e10f',
                'date': '20160127T102626-0800',
                'id': 182247,
            },
            {
                'username': 'bradd',
                'version': 'd61d8c623347d90d5',
                'date': '20160126T144727-0800',
                'id': 181491,
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/'),
        json=changes_json, status=200,
        content_type='application/json',
    )

    changes = tc.changes.all().filter(
        build=802245,
        count=2,
    )
    assert len(changes) == 2
    assert changes[0].id == 182247
    assert changes[0].version == '124b46cb36a05e10f'
    assert changes[1].id == 181491
    assert changes[1].version == 'd61d8c623347d90d5'


@responses.activate
def test_filter_by_vcs_root():
    changes_json = {
        'count': 2,
        'change': [
            {
                'username': 'xiaomengw',
                'version': '362758f170d889d55',
                'date': '20160817T232334-0700',
                'id': 314798,
            },
            {
                'username': 'xiaomeng w',
                'version': 'ea59bd8f32b6d5bfb',
                'date': '20160817T230716-0700',
                'id': 314797,
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/'),
        json=changes_json, status=200,
        content_type='application/json',
    )

    changes = tc.changes.all().filter(
        vcs_root='AppRouter_Inventory',
        count=2,
    )
    assert len(changes) == 2
    assert changes[0].id == 314798
    assert changes[0].version == '362758f170d889d55'
    assert changes[1].id == 314797
    assert changes[1].version == 'ea59bd8f32b6d5bfb'


@responses.activate
def test_filter_by_username():
    changes_json = {
        'count': 2,
        'change': [
            {
                'username': 'marca',
                'href': '/httpAuth/app/rest/changes/id:314330',
                'version': '09f63026bad685bc44bbf6b44ba35f8eb18748ca',
                'date': '20160817T111443-0700',
                'id': 314330,
            },
            {
                'username': 'marca',
                'href': '/httpAuth/app/rest/changes/id:314329',
                'version': '09f63026bad685bc44bbf6b44ba35f8eb18748ca',
                'date': '20160817T111443-0700',
                'id': 314329,
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/'),
        json=changes_json, status=200,
        content_type='application/json',
    )

    changes = tc.changes.all().filter(
        username='marca',
        count=2,
    )
    assert len(changes) == 2
    assert changes[0].id == 314330
    assert changes[0].version == '09f63026bad685bc44bbf6b44ba35f8eb18748ca'
    assert changes[1].id == 314329
    assert changes[1].version == '09f63026bad685bc44bbf6b44ba35f8eb18748ca'


@responses.activate
def test_filter_by_version():
    changes_json = {
        'count': 2,
        'change': [
            {
                'username': 'marca',
                'href': '/httpAuth/app/rest/changes/id:314330',
                'version': '09f63026bad685bc44bbf6b44ba35f8eb18748ca',
                'date': '20160817T111443-0700',
                'id': 314330,
            },
            {
                'username': 'marca',
                'href': '/httpAuth/app/rest/changes/id:314329',
                'version': '09f63026bad685bc44bbf6b44ba35f8eb18748ca',
                'date': '20160817T111443-0700',
                'id': 314329,
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/changes/'),
        json=changes_json, status=200,
        content_type='application/json',
    )

    changes = tc.changes.all().filter(
        version='09f63026bad685bc44bbf6b44ba35f8eb18748ca',
        count=2,
    )
    assert len(changes) == 2
    assert changes[0].id == 314330
    assert changes[0].version == '09f63026bad685bc44bbf6b44ba35f8eb18748ca'
    assert changes[1].id == 314329
    assert changes[1].version == '09f63026bad685bc44bbf6b44ba35f8eb18748ca'
