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

### Get all projects in server

```python
tc.get_all_projects()
```

More examples to come...
