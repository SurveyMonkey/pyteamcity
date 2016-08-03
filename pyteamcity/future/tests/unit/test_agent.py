from pyteamcity.future import Agent, AgentQuerySet, TeamCity

tc = TeamCity.from_environ()


def get_agent_quick(id):
    query_set = AgentQuerySet(tc)
    return Agent.from_dict({'id': id}, query_set)


def test_unit_get_all():
    agents = tc.agents.all()
    assert agents._get_url().endswith('/app/rest/agents/')


def test_unit_get_by_id():
    url = tc.agents.all().get(id=34, just_url=True)
    assert url.endswith('/agents/id:34')


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
