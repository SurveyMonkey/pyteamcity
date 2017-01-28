import responses

from pyteamcity.future import TeamCity
from pyteamcity.future.agent import Agent, AgentQuerySet

tc = TeamCity()


def get_agent_quick(id):
    query_set = AgentQuerySet(tc)
    return Agent.from_dict({'id': id}, query_set)


def test_unit_get_all():
    agents = tc.agents.all()
    assert agents._get_url().endswith('/app/rest/agents/')


def test_unit_get_by_id():
    url = tc.agents.all().get(id=34, just_url=True)
    assert url.endswith('/agents/id:34')


@responses.activate
def test_unit_get_all_with_responses():
    agents_json = {
        "count": 6,
        "href": "/httpAuth/app/rest/agents/",
        "agent": [
            {"id": 69, "name": "tcagent101"},
            {"id": 67, "name": "tcagent102"},
            {"id": 70, "name": "tcagent103"},
            {"id": 34, "name": "tcagent112"},
            {"id": 32, "name": "tcagent113"},
            {"id": 33, "name": "tcagent114"},
        ],
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agents/'),
        json=agents_json, status=200,
        content_type='application/json',
    )
    agents = tc.agents.all()
    assert len(agents) == 6
    for agent in agents:
        assert hasattr(agent, 'name')


@responses.activate
def test_unit_delete_agent():
    agent_json = {'id': 34, 'name': 'tcagent112'}
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agents/id:34'),
        json=agent_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.DELETE,
        tc.relative_url('app/rest/agents/id:34'),
        json=agent_json, status=204,
        content_type='application/json',
    )
    agent = tc.agents.all().get(id=34)
    req = agent.delete(dry_run=True)
    assert req.method == 'DELETE'
    assert req.headers['Content-Type'] == 'text/plain'
    assert req.headers['Accept'] == 'text/plain'
    assert req.url.endswith('/agents/id:34')
    agent.delete()


@responses.activate
def test_unit_get_by_id_with_responses():
    agent_pools_json = {
        "id": 0,
        "name": "Default",
        "href": "/httpAuth/app/rest/agentPools/id:0",
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agentPools/id:0'),
        json=agent_pools_json, status=200,
        content_type='application/json',
    )
    agent_json = {
        'id': 34,
        'name': 'tcagent112',
        'pool': {'id': 0, 'name': 'Default'},
        "properties": {
            "count": 2,
            "property": [
                {'name': 'env.TEAMCITY_GIT_PATH', 'value': '/usr/bin/git'},
                {'name': 'env.TERM', 'value': 'linux'},
            ],
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/agents/id:34'),
        json=agent_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.PUT,
        tc.relative_url('app/rest/agents/id:34/enabled'),
        body='true', status=200,
        content_type='text/plain',
    )
    agent = tc.agents.all().get(id=34)
    assert agent.id == 34
    assert agent.name == 'tcagent112'
    assert agent.pool.name == 'Default'
    assert 'tcagent112' in repr(agent)
    params = agent.parameters_dict
    assert params['env.TEAMCITY_GIT_PATH'].value == '/usr/bin/git'
    assert params['env.TERM'].value == 'linux'

    # Enable agent
    agent.enable()


def test_unit_disable_enable():
    agent = get_agent_quick(id=34)

    req = agent.disable(dry_run=True)
    assert req.method == 'PUT'
    assert req.headers['Content-Type'] == 'text/plain'
    assert req.headers['Accept'] == 'text/plain'
    assert req.body == 'false'
    assert req.url.endswith('/agents/id:34/enabled')

    req = agent.enable(dry_run=True)
    assert req.method == 'PUT'
    assert req.headers['Content-Type'] == 'text/plain'
    assert req.headers['Accept'] == 'text/plain'
    assert req.body == 'true'
    assert req.url.endswith('/agents/id:34/enabled')


def test_unit_get_by_name():
    url = tc.agents.all().get(name='tcagent112', just_url=True)
    assert url.endswith('/agents/name:tcagent112')


def test_unit_filter_by_connected():
    agents = tc.agents.all().filter(connected=True)
    assert agents._get_url().endswith('/agents/?locator=connected:True')

    agents = tc.agents.all().filter(connected=False)
    assert agents._get_url().endswith('/agents/?locator=connected:False')


def test_unit_filter_by_authorized():
    agents = tc.agents.all().filter(authorized=True)
    assert agents._get_url().endswith('/agents/?locator=authorized:True')

    agents = tc.agents.all().filter(authorized=False)
    assert agents._get_url().endswith('/agents/?locator=authorized:False')


def test_unit_filter_by_enabled():
    agents = tc.agents.all().filter(enabled=True)
    assert agents._get_url().endswith('/agents/?locator=enabled:True')

    agents = tc.agents.all().filter(enabled=False)
    assert agents._get_url().endswith('/agents/?locator=enabled:False')
