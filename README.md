# PyTeamCity

[![Latest Version](https://badge.fury.io/py/pyteamcity.svg)](https://pypi.python.org/pypi/pyteamcity/)
[![Travis CI Build Status](https://travis-ci.org/SurveyMonkey/pyteamcity.svg?branch=master)](https://travis-ci.org/SurveyMonkey/pyteamcity)
[![AppVeyor Build Status](https://ci.appveyor.com/api/projects/status/32r7s2skrgm9ubva?svg=true)](https://ci.appveyor.com/project/msabramo/pyteamcity-v7gx2)
[![Coveralls Coverage Status](https://coveralls.io/repos/github/SurveyMonkey/pyteamcity/badge.svg?branch=master)](https://coveralls.io/github/SurveyMonkey/pyteamcity?branch=master)

Python interface to the [REST
API](https://confluence.jetbrains.com/display/TCD9/REST+API) of
[TeamCity](https://www.jetbrains.com/teamcity/)

## Installation

```
pip install pyteamcity
```

## New API work-in-progress

Note that I am working on a new API currently called
[pyteamcity.future](https://github.com/SurveyMonkey/pyteamcity/blob/master/pyteamcity/future)
(initially added in
[#37](https://github.com/SurveyMonkey/pyteamcity/pull/37)).

Goal here is to create a brand new API that is much more flexible and to
have nicer code that is easier to work with. The old code encourages
adding a zillion methods for different ways of filtering. The new code
has an API with a smaller number of methods that are more consistent and
more flexible in terms of filtering. It is modeled after the Django ORM
API.

There's no formal docs for this API yet, but you should be able to
figure out how to use it by looking at the [unit
tests](https://github.com/SurveyMonkey/pyteamcity/tree/master/pyteamcity/future/tests/unit).

I am probably not going to merge PRs that add things to the old API,
because I see the new API as the future. I of course am very interested
in PRs that add things to the new API!

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
tc.get_projects()
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

You can also look at
[sample.py](https://github.com/SurveyMonkey/pyteamcity/blob/master/sample.py) or
[test_legacy.py](https://github.com/SurveyMonkey/pyteamcity/blob/master/pyteamcity/legacy/test_legacy.py)

## Acknowledgements

This is a heavily-modified fork of https://github.com/yotamoron/teamcity-python-rest-client so many thanks are due to [Yotam Oron](https://github.com/yotamoron)
