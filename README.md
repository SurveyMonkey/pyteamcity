# TeamCity Python REST Client

## What it does

This code can be used to easily access the [REST
API](https://confluence.jetbrains.com/display/TCD9/REST+API) of
[TeamCity](https://www.jetbrains.com/teamcity/) and make sure any
requests are well-formed, easily.

## Installation

To install simply clone the repository, and then add the folder `teamcity-python-rest-client` to your build path in your selected IDE.

Using PyCharm this is done by going to __Settings__ `->` __Project Interpreter__ `->` Click the cog `->` Click on "show path for selected interpreter.".

There you can add the folder to the current selected interpreter, which will make it available for your projects to use locally. In your server, you will have to place tc.py inside your Python libraries directory (in case of my CentOS installation, this is in `/usr/lib/python2.6/site-packages`).

## Examples

### Connect to server

```python
# This initialises the Client with the settings passed. <port> has to be an integer.
client = TeamCityRESTApiClient('account', 'password', 'server', <port>)
```

or specify no parameters and it will read settings from environment
variables:

- `TEAMCITY_USER`
- `TEAMCITY_PASSWORD`
- `TEAMCITY_HOST`
- `TEAMCITY_PORT` (Defaults to 80 if not set)

```python
# Initialises with environment variables: TEAMCITY_{USER,PASSWORD,HOST,PORT}
client = TeamCityRESTApiClient()
```

### Get all projects in server

```python
# Specify the resource type we are going to get, in this case <projects>
client.get_all_projects()

# Make the cURL request and get data back as a dictionary.
client.get_from_server()
```

### Get all builds from a build type

Getting all builds from anywhere can potentially give you a very large response back, which is why we give you the ability to only make the request for a certain number of elements, and also specify where to start from.

This start and count then lets you go through all the builds while never getting them all at the same time.

```python
# Specify how many returns per request and your BuildType ID
ct = 50
buildTypeId = "bt[0-9]+"

# Get the first set of responses
client.get_all_builds_by_build_type_id(buildTypeId, start=0, count=ct)
response = client.get_from_server()

# Loop through until the response doesn't contain a count of builds (which should be == ct)
i = ct
while response.keys()[0] == "count":
	client.get_all_builds_by_build_type_id(buildTypeId, start=i, count=ct)
	i += ct
	response = client.get_from_server()
```

More examples to come...
