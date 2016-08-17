import responses

from pyteamcity.future import TeamCity

tc = TeamCity()


def test_unit_get_all():
    agent_pools = tc.agent_pools.all()
    assert agent_pools._get_url().endswith('/app/rest/agentPools/')


@responses.activate
def test_unit_get_all_with_responses():
    agent_pools_json = {
        "count": 3,
        "href": "/httpAuth/app/rest/agentPools",
        "agentPool": [
            {
                "id": 6,
                "name": "PHP agent",
                "href": "/httpAuth/app/rest/agentPools/id:6",
            },
            {
                "id": 4,
                "name": "Production",
                "href": "/httpAuth/app/rest/agentPools/id:4",
            },
            {
                "id": 0,
                "name": "Default",
                "href": "/httpAuth/app/rest/agentPools/id:0",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agentPools/'),
        json=agent_pools_json, status=200,
        content_type='application/json',
    )
    agent_pools = tc.agent_pools.all()
    for agent_pool in agent_pools:
        assert hasattr(agent_pool, 'name')


@responses.activate
def test_unit_filter_by_name_with_responses():
    agent_pools_json = {
        "count": 1,
        "href": "/httpAuth/app/rest/agentPools",
        "agentPool": [
            {
                "id": 6,
                "name": "PHP agent",
                "href": "/httpAuth/app/rest/agentPools/id:6",
            },
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agentPools/'),
        json=agent_pools_json, status=200,
        content_type='application/json',
    )
    agent_pools = tc.agent_pools.all().filter(name='PHP agent')
    assert len(agent_pools) == 1
    assert agent_pools[0].name == 'PHP agent'


@responses.activate
def test_unit_get_one_with_responses():
    agent_pool_json = {
        "id": 6,
        "name": "PHP agent",
        "href": "/httpAuth/app/rest/agentPools/id:6",
        "projects": {
            "count": 4,
            "project": [
                {
                    "id": "Wufoo",
                    "name": "wufoo",
                    "parentProjectId": "_Root",
                },
                {
                    "id": "Cmsweb_ReleaseToMt1Unified",
                    "name": "release to MT1",
                    "parentProjectId": "Cmsweb",
                },
                {
                    "id": "Cmsweb_Build",
                    "name": "Build",
                    "parentProjectId": "Cmsweb",
                },
                {
                    "id": "Cmsweb_ReleaseToMt2Unified",
                    "name": "release to MT2",
                    "parentProjectId": "Cmsweb",
                },
            ],
        },
        "agents": {
            "count": 1,
            "agent": [
                {
                    "id": 40,
                    "name": "tcagent117",
                    "typeId": 40,
                    "href": "/httpAuth/app/rest/agents/id:40",
                },
            ],
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agentPools/id:6'),
        json=agent_pool_json, status=200,
        content_type='application/json',
    )
    agent_pool = tc.agent_pools.all().get(id=6)
    assert agent_pool.name == 'PHP agent'
    assert len(agent_pool.agents) == 1
    assert agent_pool.agents[0].name == 'tcagent117'
    assert len(agent_pool.projects) == 4
    assert agent_pool.projects[0].name == 'wufoo'
    assert 'PHP agent' in repr(agent_pool)


def test_unit_get_by_id():
    url = tc.agent_pools.all().get(id=4, just_url=True)
    assert url.endswith('/agentPools/id:4')
