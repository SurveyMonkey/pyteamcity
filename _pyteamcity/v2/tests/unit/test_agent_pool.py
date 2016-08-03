from _pyteamcity import v2

tc = v2.TeamCity.from_environ()


def test_unit_get_all():
    agent_pools = tc.agent_pools.all()
    assert agent_pools._get_url().endswith('/app/rest/agentPools/')


def test_unit_get_by_id():
    url = tc.agent_pools.all().get(id=4, just_url=True)
    assert url.endswith('/agentPools/id:4')
