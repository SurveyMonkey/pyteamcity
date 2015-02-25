# PyTeamCity

[![Latest Version](https://pypip.in/version/pyteamcity/badge.svg)](https://pypi.python.org/pypi/pyteamcity/)
[![Build Status](https://travis-ci.org/SurveyMonkey/pyteamcity.svg?branch=master)](https://travis-ci.org/SurveyMonkey/pyteamcity)

Python interface to the [REST
API](https://confluence.jetbrains.com/display/TCD9/REST+API) of
[TeamCity](https://www.jetbrains.com/teamcity/)

## Installation

```
pip install pyteamcity
```

## Examples

### Connect to server

```python
from pyteamcity import TeamCity

# This initialises the Client with the settings passed. <port> has to be an integer.
tc = TeamCity('account', 'password', 'server', <port>)
```

or specify no parameters and it will read settings from environment
variables:

- `TEAMCITY_USER`
- `TEAMCITY_PASSWORD`
- `TEAMCITY_HOST`
- `TEAMCITY_PORT` (Defaults to 80 if not set)

```python
from pyteamcity import TeamCity

# Initialises with environment variables: TEAMCITY_{USER,PASSWORD,HOST,PORT}
tc = TeamCity()
```

### Getting data

```python
tc.get_all_projects()
tc.get_project_by_project_id('MyProject')
tc.get_all_users()
tc.get_user_by_username('codyw')
tc.get_all_vcs_roots()
tc.get_all_build_types()
tc.get_changes_by_build_id(73450)
tc.get_build_statistics_by_build_id(73450)
tc.get_build_tags_by_build_id(73450)
tc.get_all_changes()
tc.get_change_by_change_id(16884)
tc.get_all_builds(start=0, count=3)
tc.get_build_by_build_id(73450)
tc.get_server_info()
tc.get_agents()
tc.get_all_plugins()
```

You can also look at [sample.py](sample.py) or
[test_pyteamcity.py](test_pyteamcity.py)

## Acknowledgements

This is a heavily-modified fork of https://github.com/yotamoron/teamcity-python-rest-client so many thanks are due to [Yotam Oron](https://github.com/yotamoron)
