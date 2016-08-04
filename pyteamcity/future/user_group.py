from .core.queryset import QuerySet


class UserGroup(object):
    def __init__(self, key,
                 name, description, href,
                 query_set, data_dict=None):
        self.key = key
        self.name = name
        self.description = description
        self.href = href
        self.query_set = query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: key=%r name=%r description=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.key,
            self.name,
            self.description)

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            key=d.get('key'),
            name=d.get('name'),
            description=d.get('description'),
            href=d.get('href'),
            query_set=query_set,
            data_dict=d)

    @property
    def users(self):
        from .user import User

        ret = []
        for user in self._data_dict['users']['user']:
            ret.append(User.from_dict(user))
        return ret


class UserGroupQuerySet(QuerySet):
    uri = '/app/rest/userGroups/'
    _entity_factory = UserGroup

    def filter(self, key=None, name=None):
        if key is not None:
            self._add_pred('key', key)
        if name is not None:
            self._add_pred('name', name)
        return self

    def __iter__(self):
        return (self.__class__._entity_factory.from_dict(d, self)
                for d in self._data()['group'])
