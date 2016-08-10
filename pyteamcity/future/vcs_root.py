from .core.queryset import QuerySet


class VCSRoot(object):
    def __init__(self, id,
                 name, href,
                 query_set, data_dict=None):
        self.id = id
        self.name = name
        self.href = href
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
            name=d.get('name'),
            href=d.get('href'),
            query_set=query_set,
            data_dict=d)


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
