import json

from pyteamcity import TeamCity

tc = TeamCity()

# data = tc.get_all_users()
# print(json.dumps(data, indent=4))

# data = tc.get_user_by_username('codyw')
# print(json.dumps(data, indent=4))

# data = tc.get_all_vcs_roots()
# print(json.dumps(data, indent=4))

# data = tc.get_vcs_root_by_vcs_root_id('CodeRepo')
# print(json.dumps(data, indent=4))

# data = tc.get_all_build_types()
# print(json.dumps(data, indent=4))

# data = tc.get_changes_by_build_id(73450)
# print(json.dumps(data, indent=4))

# data = tc.get_build_statistics_by_build_id(73450)
# print(json.dumps(data, indent=4))

# data = tc.get_build_tags_by_build_id(73450)
# print(json.dumps(data, indent=4))

# data = tc.get_change_by_change_id(16884)
# print(json.dumps(data, indent=4))

# data = tc.get_all_changes()
# print(json.dumps(data, indent=4))

# data = tc.get_build_by_build_id(73450)
# print(json.dumps(data, indent=4))

data = tc.get_projects()
print(json.dumps(data, indent=4))

# data = tc.get_agents()
# print(json.dumps(data, indent=4))

# data = tc.get_agent_by_agent_id(41)
# print(json.dumps(data, indent=4))

# data = tc.get_build_type(build_type_id='Teamcity_TriggerFullBackup')
# print(json.dumps(data, indent=4))

# data = tc.get_all_builds_by_build_type_id(
#     build_type_id='Teamcity_TriggerFullBackup', start=0, count=3)
# print(json.dumps(data, indent=4))

# data = tc.get_all_builds(start=0, count=3)
# print(json.dumps(data, indent=4))

# data = tc.get_all_plugins()
# print(json.dumps(data, indent=4))

# data = tc.get_server_info()
# print(json.dumps(data, indent=4))

# data = tc.get_all_projects()
# print(json.dumps(data, indent=4))

# data = tc.get_project_by_project_id('Usercontentsvc_ReleaseToMt5')
# print(json.dumps(data, indent=4))

# url = tc.get_project_by_project_id.get_url('Usercontentsvc_ReleaseToMt5')
# print(url)

# url = tc.get_project_by_project_id(
#     'Usercontentsvc_ReleaseToMt5', return_type='url')
# print(url)

# url = tc.get_project_by_project_id(
#     'Usercontentsvc_ReleaseToMt5', return_type='request')
# print(url)
