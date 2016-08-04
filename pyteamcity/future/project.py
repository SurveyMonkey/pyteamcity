from .core.parameter import Parameter
from .core.queryset import QuerySet
from .core.web_browsable import WebBrowsable


class Project(WebBrowsable):
    def __init__(self, id, name, description,
                 href, web_url, parent_project_id,
                 project_query_set,
                 data_dict=None):
        self.id = id
        self.name = name
        self.description = description
        self.href = href
        self.web_url = web_url
        self.parent_project_id = parent_project_id
        self.project_query_set = project_query_set
        self._data_dict = data_dict

    def __repr__(self):
        return '<%s.%s: id=%r name=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.name)

    @classmethod
    def from_dict(cls, d, project_query_set=None):
        return Project(
            id=d.get('id'),
            name=d.get('name'),
            description=d.get('description'),
            href=d.get('href'),
            web_url=d.get('webUrl'),
            parent_project_id=d.get('parentProjectId'),
            project_query_set=project_query_set,
            data_dict=d)

    @property
    def build_types(self):
        from .build_type import BuildTypeQuerySet

        teamcity = self.project_query_set.teamcity
        return BuildTypeQuerySet(teamcity).filter(project_id=self.id)

    @property
    def projects(self):
        teamcity = self.project_query_set.teamcity
        project_query_set = ProjectQuerySet(teamcity)
        project_query_set._data_dict = self._data_dict['projects']
        return project_query_set

    @property
    def parent_project(self):
        teamcity = self.project_query_set.teamcity
        return ProjectQuerySet(teamcity).get(id=self.parent_project_id)

    @property
    def parameters_dict(self):
        d = {}

        for param in self._data_dict['parameters']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            if 'type' in param:
                param_obj.ptype = param['type']
            d[param['name']] = param_obj

        return d


class ProjectQuerySet(QuerySet):
    uri = '/app/rest/projects/'
    _entity_factory = Project

    def filter(self, id=None, name=None):
        if id is not None:
            self._add_pred('id', id)
        if name is not None:
            self._add_pred('name', name)
        return self

    def __iter__(self):
        return (Project.from_dict(d, self) for d in self._data()['project'])
