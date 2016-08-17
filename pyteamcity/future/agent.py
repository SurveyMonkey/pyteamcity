import requests

from .core.parameter import Parameter
from .core.queryset import QuerySet

from .agent_pool import AgentPoolQuerySet


class Agent(object):
    """
    (Pdb++) agent._data_dict.keys()
    [u'typeId', u'name', u'ip', u'enabled', u'properties',
     u'uptodate', u'href', u'connected', u'authorized',
     u'id', u'pool']
    """

    def __init__(self, id, href, name, type_id, ip,
                 enabled, connected, authorized,
                 pool_id,
                 query_set, data_dict=None):
        self.id = id
        self.href = href
        self.name = name
        self.type_id = type_id
        self.ip = ip
        self.enabled = enabled
        self.connected = connected
        self.authorized = authorized
        self.pool_id = pool_id
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
            type_id=d.get('typeId'),
            ip=d.get('ip'),
            enabled=d.get('enabled'),
            connected=d.get('connected'),
            authorized=d.get('authorized'),
            pool_id=d.get('pool', {}).get('id'),
            query_set=query_set,
            data_dict=d)

    @property
    def pool(self):
        teamcity = self.query_set.teamcity
        agent_pool = AgentPoolQuerySet(teamcity).get(id=self.pool_id)
        return agent_pool

    @property
    def parameters_dict(self):
        d = {}

        for param in self._data_dict['properties']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            d[param['name']] = param_obj

        return d

    @property
    def teamcity(self):
        return self.query_set.teamcity

    def set_enabled(self, enabled_str, dry_run=False):
        extra_headers = {'Content-Type': 'text/plain',
                         'Accept': 'text/plain'}
        req = self._put_request('enabled', data=enabled_str,
                                extra_headers=extra_headers)
        if dry_run:
            return req
        return self.teamcity.session.send(req)

    def _put_request(self, relative_uri, data, extra_headers):
        url = self._get_url() + '/' + relative_uri
        headers = dict(self.teamcity.session.headers)
        headers.update(extra_headers)
        req = requests.Request(
            method='PUT',
            url=url,
            data=data,
            headers=headers)
        prepped = self.teamcity.session.prepare_request(req)
        return prepped

    def _get_url(self):
        return AgentQuerySet(self.teamcity).get(id=self.id, just_url=True)

    def enable(self, dry_run=False):
        return self.set_enabled('true', dry_run=dry_run)

    def disable(self, dry_run=False):
        return self.set_enabled('false', dry_run=dry_run)


class AgentQuerySet(QuerySet):
    uri = '/app/rest/agents/'
    _entity_factory = Agent

    def filter(self, id=None, name=None,
               connected=None, authorized=None, enabled=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        if connected is not None:
            self._add_pred('connected', connected)
        if authorized is not None:
            self._add_pred('authorized', authorized)
        if enabled is not None:
            self._add_pred('enabled', enabled)
        return self

    def __iter__(self):
        return (self._entity_factory.from_dict(d, self)
                for d in self._data()['agent'])
