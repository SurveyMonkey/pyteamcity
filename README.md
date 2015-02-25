# PyTeamCity

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
from teamcityrestapiclient import TeamCityRESTApiClient

# This initialises the Client with the settings passed. <port> has to be an integer.
tc = TeamCityRESTApiClient('account', 'password', 'server', <port>)
```

or specify no parameters and it will read settings from environment
variables:

- `TEAMCITY_USER`
- `TEAMCITY_PASSWORD`
- `TEAMCITY_HOST`
- `TEAMCITY_PORT` (Defaults to 80 if not set)

```python
from teamcityrestapiclient import TeamCityRESTApiClient

# Initialises with environment variables: TEAMCITY_{USER,PASSWORD,HOST,PORT}
tc = TeamCityRESTApiClient()
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
[test_stuff.py](test_stuff.py)
