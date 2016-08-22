from . import exceptions
from .core.parameter import Parameter
from .core.queryset import QuerySet


class VCSRoot(object):
    def __init__(self, id,
                 name, href,
                 teamcity, query_set, data_dict=None):
        self.id = id
        self.name = name
        self.href = href
        self.teamcity = teamcity
        self.query_set = query_set
        if self.teamcity is None and self.query_set is not None:
            self.teamcity = self.query_set.teamcity
        self._data_dict = data_dict

    @property
    def url(self):
        return self.properties['url'].value

    @property
    def branch(self):
        return self.properties['branch'].value

    @property
    def branch_spec(self):
        return self.properties['teamcity:branchSpec'].value

    def __repr__(self):
        return '<%s.%s: id=%r name=%r url=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name,
            self.url,
        )

    @classmethod
    def from_dict(cls, d, query_set=None, teamcity=None):
        return cls(
            id=d.get('id'),
            name=d.get('name'),
            href=d.get('href'),
            query_set=query_set,
            teamcity=teamcity,
            data_dict=d)

    @property
    def properties(self):
        d = {}

        for param in self._data_dict['properties']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            d[param['name']] = param_obj

        return d

    def delete(self):
        url = self.teamcity.base_base_url + self.href
        res = self.teamcity.session.delete(url)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)


class VCSRootQuerySet(QuerySet):
    uri = '/app/rest/vcs-roots/'
    _entity_factory = VCSRoot

    def filter(self, id=None, name=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        return self

    def __iter__(self):
        return (self.__class__._entity_factory.from_dict(d, self)
                for d in self._data()['vcs-root'])

    def create(self,
               name, vcs_name, url, branch, branch_spec='',
               id=None,
               parent_project_locator='id:_Root',
               agent_clean_files_policy='ALL_UNTRACKED',
               agent_clean_policy='ALWAYS',
               auth_method='PASSWORD',
               ignore_known_hosts=True,
               submodule_checkout='CHECKOUT',
               use_alternates=True,
               user_for_tags='teamcity',
               username='teamcity',
               username_style='USERID'):
        _url = self.base_url
        vcs_root_json = {
            'name': name,
            'vcsName': vcs_name,
            'id': id,
            'properties': {
                'property': [
                    {'name': 'agentCleanFilesPolicy',
                     'value': agent_clean_files_policy},
                    {'name': 'agentCleanPolicy',
                     'value': agent_clean_policy},
                    {'name': 'authMethod',
                     'value': auth_method},
                    {'name': 'branch',
                     'value': branch},
                    {'name': 'ignoreKnownHosts',
                     'value': 'true' if ignore_known_hosts else 'false'},
                    {'name': 'secure:password'},
                    {'name': 'submoduleCheckout',
                     'value': submodule_checkout},
                    {'name': 'teamcity:branchSpec',
                     'value': branch_spec},
                    {'name': 'url',
                     'value': url},
                    {'name': 'useAlternates',
                     'value': 'true' if use_alternates else 'false'},
                    {'name': 'userForTags',
                     'value': user_for_tags},
                    {'name': 'username',
                     'value': username},
                    {'name': 'usernameStyle',
                     'value': username_style},
                ],
            },
            'project': {'id': '_Root'},
        }
        res = self.teamcity.session.post(
            url=_url,
            headers={'Content-Type': 'application/json'},
            allow_redirects=False,
            json=vcs_root_json)
        if not res.ok:
            raise exceptions.HTTPError(
                status_code=res.status_code,
                reason=res.reason,
                text=res.text)
        vcs_root = VCSRoot.from_dict(
            res.json(),
            teamcity=self.teamcity,
        )
        return vcs_root
