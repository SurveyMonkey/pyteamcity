import json
import os

from teamcityrestapiclient import TeamCityRESTApiClient

tc = TeamCityRESTApiClient()
tc.get_server_info()
print(json.dumps(tc.get_from_server(), indent=4))
