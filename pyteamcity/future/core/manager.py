class Manager(object):
    def __init__(self, teamcity, query_set_factory):
        self.teamcity = teamcity
        self.query_set_factory = query_set_factory

    def all(self):
        return self.query_set_factory(teamcity=self.teamcity)
