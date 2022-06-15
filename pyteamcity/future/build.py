from six.moves.urllib.parse import quote
import tempfile
import os

from . import exceptions
from .core.parameter import Parameter
from .core.queryset import QuerySet
from .core.utils import parse_date_string, raise_on_status

from .agent import Agent
from .artifact import Artifact
from .build_type import BuildTypeQuerySet
from .project import ProjectQuerySet
from .user import User
from .build_statistics import BuildStatistics
from .test_occurrences import TestOccurrences


class Build(object):
    def __init__(self, id, number,
                 build_type_id,
                 queued_date_string, start_date_string, finish_date_string,
                 state, status, branch_name, href,
                 build_query_set, teamcity, data_dict=None):
        self.id = id
        self.number = number
        self.queued_date_string = queued_date_string
        self.start_date_string = start_date_string
        self.finish_date_string = finish_date_string
        self.build_type_id = build_type_id
        self.state = state
        self.status = status
        self.branch_name = branch_name
        self.href = href
        self.build_query_set = build_query_set
        self.teamcity = teamcity
        if self.teamcity is None and self.build_query_set is not None:
            self.teamcity = self.build_query_set.teamcity
        self._data_dict = data_dict

    @property
    def data(self):
        return self._data_dict

    @property
    def user(self):
        if 'user' in self._data_dict.get('triggered', {}):
            return User.from_dict(self._data_dict['triggered']['user'])

    @property
    def dependencies(self):
        if 'build' in self._data_dict.get('snapshot-dependencies', {}):
            return [Build.from_dict(b) for b in self._data_dict['snapshot-dependencies']['build']]
        return []

    @property
    def queued_date(self):
        return parse_date_string(self.queued_date_string)

    @property
    def start_date(self):
        if self.state == "queued":
            return parse_date_string(self._data_dict.get("startEstimate", None))
        return parse_date_string(self.start_date_string)

    @property
    def finish_date(self):
        #running build there will not be finish date
        return parse_date_string(self.finish_date_string) if self.finish_date_string  else None
    
    @property
    def status_text(self):
        return self._data_dict.get('statusText')
    
    @property
    def wait_reason(self):
        return self._data_dict.get('waitReason', "")
    
    @property
    def test_occurances(self):
        return TestOccurrences.from_dict(self.id, self._data_dict.get('testOccurrences', {}))

    @property
    def agent(self):
        return Agent.from_dict(self._data_dict.get('agent'))

    @property
    def build_type(self):
        teamcity = self.build_query_set.teamcity
        build_type_id = self._data_dict['buildTypeId']
        build_type = BuildTypeQuerySet(teamcity).get(id=build_type_id)

        return build_type
    
    @property
    def project(self):
        teamcity = self.build_query_set.teamcity
        project_id = self._data_dict.get('buildType', {}).get('projectId')
        return ProjectQuerySet(teamcity).get(id=project_id) if project_id else None
    

    def __repr__(self):
        return '<%s.%s: id=%r build_type_id=%r number=%r>' % (
            self.__module__,
            self.__class__.__name__,
            self.id,
            self.build_type_id,
            self.number)

    def _update_dict(self, d):
        self.id=d.get('id', self.id)
        self.number=d.get('number', self.number)
        self.queued_date_string=d.get('queuedDate', self.queued_date_string)
        self.start_date_string=d.get('startDate', self.start_date_string)
        self.finish_date_string=d.get('finishDate', self.finish_date_string)
        self.build_type_id=d.get('buildTypeId', self.build_type_id)
        self.state=d.get('state', self.state)
        self.status=d.get('status', self.status)
        self.branch_name=d.get('branchName', self.branch_name)
        self.href=d.get('href', self.href)
        self._data_dict=d if d else self._data_dict

    @classmethod
    def from_dict(cls, d, build_query_set=None, teamcity=None):
        return Build(
            id=d.get('id'),
            number=d.get('number'),
            queued_date_string=d.get('queuedDate'),
            start_date_string=d.get('startDate'),
            finish_date_string=d.get('finishDate'),
            build_type_id=d.get('buildTypeId'),
            state=d.get('state'),
            status=d.get('status'),
            branch_name=d.get('branchName'),
            href=d.get('href'),
            build_query_set=build_query_set,
            teamcity=teamcity,
            data_dict=d)

    @property
    def parameters_dict(self):
        d = {}

        for param in self._data_dict['properties']['property']:
            param_obj = Parameter()
            if 'value' in param:
                param_obj.value = param['value']
            if 'type' in param:
                param_obj.ptype = param['type']
            d[param['name']] = param_obj

        return d

    @property
    def api_url(self):
        teamcity = self.build_query_set.teamcity
        base_url = teamcity.base_url
        url = base_url + '/app/rest/builds/id:%s' % self.id
        return url

    @property
    def artifacts(self):
        return Artifact(build=self)

    @property
    def build_log(self):
        return self.get_build_log(archived=False, content_length=None)

    def get_build_log(self, archived=False, content_length=None):
        url = '/downloadBuildLog.html?buildId=%s' % self.id
        url = self.teamcity.base_url + url

        if archived:
            url = url + '&archived=true'

        if content_length:
            res = self.teamcity.session.head(url)
            raise_on_status(res)

            msg_size = int(res.headers['Content-Length'])
            if msg_size > content_length:
                err = 'build.log content-length exceeded (%s > %s)'
                err = err % (msg_size, content_length)
                raise exceptions.ArtifactSizeExceeded(err)

        res = self.teamcity.session.get(url)
        raise_on_status(res)
        return res.text
    
    def get_build_log_file(self, archived=False):
        url = '/downloadBuildLog.html?buildId=%s' % self.id
        url = self.teamcity.base_url + url
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = tmp
        
        os.makedirs(tmp_dir)
        log_file = os.path.join(tmp_dir, "tc_log_" + str(self.id))
        
        if archived:
            url = url + '&archived=true'
        with self.teamcity.session.get(url, stream=True) as res:
            raise_on_status(res)
            with open(log_file, 'wb') as f:
                for chunk in res.iter_content(chunk_size=8192):
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    f.write(chunk)
        
        return log_file

    def refresh(self):
        res = self.teamcity.session.get(self.api_url)
        raise_on_status(res)
        data = res.json() 
        return self._update_dict(data)
    
    def statistics(self):
        res = self.teamcity.session.get(self.api_url+"/statistics")
        raise_on_status(res)
        data = res.json() 
        return BuildStatistics.from_dict(self.id, data)
        
    @property
    def pinned(self):
        url = self.teamcity.base_base_url + self.href + '/pin'
        res = self.teamcity.session.get(url=url, headers={'Accept': None})
        raise_on_status(res)
        return res.text == 'true'

    def pin(self, comment):
        url = self.teamcity.base_base_url + self.href + '/pin'
        res = self.teamcity.session.put(url=url, data=comment, headers={'Accept': None})
        raise_on_status(res)
        return self

    def unpin(self):
        url = self.teamcity.base_base_url + self.href + '/pin'
        res = self.teamcity.session.delete(url=url, headers={'Accept': None})
        raise_on_status(res)
        return self


class BuildQuerySet(QuerySet):
    uri = '/app/rest/builds/'
    _entity_factory = Build

    def filter(self,
               id=None,
               project=None, affected_project=None,
               build_type=None, number=None, branch=None, user=None,
               tags=None, pinned=None,
               since_build=None, since_date=None, status=None,
               start_date_from=None, finish_date_from=None,
               agent_name=None, personal=None,
               canceled=None, failed_to_start=None, running=None,
               start=None, count=None, lookup_limit=None,
               default_filter=None, snapshots_from=None, snapshots_to=None):
        if id is not None:
            self._add_pred('id', id)
        if project is not None:
            self._add_pred('project', '(%s)' % project)
        if affected_project is not None:
            self._add_pred('affectedProject', '(%s)' % affected_project)
        if build_type is not None:
            self._add_pred('buildType', build_type)
        if number is not None:
            self._add_pred('number', number)
        if branch is not None:
            self._add_pred('branch', branch)
        if user is not None:
            self._add_pred('user', '(%s)' % user)
        if tags is not None:
            if not hasattr(tags, 'split'):
                tags = ','.join(tags)
            self._add_pred('tags', tags)
        if pinned is not None:
            self._add_pred('pinned', pinned)
        if since_build is not None:
            self._add_pred('sinceBuild', '(%s)' % since_build)
        if since_date is not None:
            since_date = self._get_since_date(since_date)
            self._add_pred('sinceDate', since_date)
        if status is not None:
            self._add_pred('status', status)
        if agent_name is not None:
            self._add_pred('agentName', agent_name)
        if personal is not None:
            self._add_pred('personal', personal)
        if canceled is not None:
            self._add_pred('canceled', canceled)
        if failed_to_start is not None:
            self._add_pred('failedToStart', failed_to_start)
        if running is not None:
            self._add_pred('running', running)
        if start is not None:
            self._add_pred('start', start)
        if count is not None:
            self._add_pred('count', count)
        if lookup_limit is not None:
            self._add_pred('lookupLimit', lookup_limit)
        if default_filter is not None:
            self._add_pred('defaultFilter', default_filter)
        if snapshots_from is not None:
            self._add_pred('snapshotDependency', "(from:%s)" % snapshots_from)
        if snapshots_to is not None:
            self._add_pred('snapshotDependency', "(to:%s)" % snapshots_to)
        if start_date_from is not None:
            self._add_pred('startDate', "(date:%s,condition:after)" % self._get_since_date(start_date_from))
        if finish_date_from is not None:
            self._add_pred('finishDate', "(date:%s,condition:after)" % self._get_since_date(finish_date_from))
        return self

    def _get_since_date(self, since_date):
        if hasattr(since_date, 'strftime'):
            since_date = since_date.strftime('%Y%m%dT%H%M%S%z')

        # If there's no timezone, assume UTC
        if '+' not in since_date:
            since_date += '+0000'

        since_date = quote(since_date)
        return since_date

    def __iter__(self):
        return (Build.from_dict(d, self, teamcity=self.teamcity)
                for d in self._data()['build'])
