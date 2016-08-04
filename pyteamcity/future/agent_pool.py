from .core.queryset import QuerySet
from .project import Project


class AgentPool(object):
    def __init__(self, id, href, name,
                 query_set, data_dict=None):
        self.id = id
        self.href = href
        self.name = name
        self.query_set = query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name)

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            id=d.get('id'),
            href=d.get('href'),
            name=d.get('name'),
            query_set=query_set,
            data_dict=d)

    @property
    def agents(self):
        from .agent import Agent

        ret = []
        for agent in self._data_dict['agents']['agent']:
            ret.append(Agent.from_dict(agent))
        return ret

    @property
    def projects(self):
        ret = []
        for project in self._data_dict['projects']['project']:
            ret.append(Project.from_dict(project))
        return ret


class AgentPoolQuerySet(QuerySet):
    uri = '/app/rest/agentPools/'
    _entity_factory = AgentPool

    def filter(self, id=None, name=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        return self

    def __iter__(self):
        return (self._entity_factory.from_dict(d, self)
                for d in self._data()['agentPool'])
