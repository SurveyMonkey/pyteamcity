# TeamCity Python REST Client

## What it does

This code can be used to easily access the REST API of TeamCity and make sure any requests are well formed, easily.

## Installation

To install simply clone the repository, and then add the folder `teamcity-python-rest-client` to your build path in your selected IDE.

Using PyCharm this is done by going to __Settings__ `->` __Project Interpreter__ `->` Click the cog `->` Click on "show path for selected interpreter.".

There you can add the folder to the current selected interpreter, which will make it available for your projects to use locally. In your server, you will have to place tc.py inside your Python libraries directory (in case of my CentOS installation, this is in `/usr/lib/python2.6/site-packages`).

## Examples

### Get all projects in server

```
# This initialises the Client with the settings passed. <port> has to be an integer.
client = TeamCityRESTApiClient('account', 'password', 'server', <port>)

# Specify the resource type we are going to get, in this case <projects>
client.get_all_projects()

# Make the cURL request and get data back as a dictionary.
client.get_from_server()
```

More examples to come...
