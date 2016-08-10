from .core.queryset import QuerySet
from .core.utils import parse_date_string


class User(object):
    def __init__(self, id,
                 username, name, email, href, last_login_string,
                 query_set, data_dict=None):
        self.id = id
        self.username = username
        self.name = name
        self.email = email
        self.href = href
        self.last_login_string = last_login_string
        self.query_set = query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r username=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.username,
            self.name)

    @property
    def last_login_date(self):
        return parse_date_string(self.last_login_string)

    @classmethod
    def from_dict(cls, d, query_set=None):
        return cls(
            id=d.get('id'),
            username=d.get('username'),
            name=d.get('name'),
            email=d.get('email'),
            href=d.get('href'),
            last_login_string=d.get('lastLogin'),
            query_set=query_set,
            data_dict=d)

    @property
    def groups(self):
        from .user_group import UserGroup

        ret = []
        for group in self._data_dict['groups']['group']:
            ret.append(UserGroup.from_dict(group))
        return ret


class UserQuerySet(QuerySet):
    uri = '/app/rest/users/'
    _entity_factory = User

    def filter(self, id=None, username=None):
        if id is not None:
            self._add_pred('id', id)
        if username is not None:
            self._add_pred('username', username)
        return self

    def __iter__(self):
        return (self.__class__._entity_factory.from_dict(d, self)
                for d in self._data()['user'])
