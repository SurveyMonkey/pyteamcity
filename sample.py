import json
import os

from teamcityrestapiclient import TeamCityRESTApiClient

user = os.getenv('TEAMCITY_USER')
password = os.getenv('TEAMCITY_PASSWORD')
host = os.getenv('TEAMCITY_HOST')
port = int(os.getenv('TEAMCITY_PORT'))

tc = TeamCityRESTApiClient(user, password, host, port)
tc.get_server_info()
print(json.dumps(tc.get_from_server(), indent=4))
