import pytest
import responses

from pyteamcity.future import exceptions, TeamCity

tc = TeamCity()


@responses.activate
def test_artifacts():
    # tc = TeamCity.from_environ()
    response_json = {
        "id": 1216841,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "126",
        "href": "/guestAuth/app/rest/builds/id:1216841",
        "artifacts": {
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/children/",
        },
    }
    response_artifacts_metadata_json = {
        "name": "",
        "modificationTime": "20160810T172802-0700",
        "href": "/guestAuth/app/rest/builds/id:1216841"
                "/artifacts/metadata/",
        "children": {
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/children/",
        }
    }
    response_artifacts_children_json = {
        "count": 7,
        "file": [
            {
                "name": "deploy_hooks",
                "modificationTime": "20160810T172802-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/deploy_hooks",
                "children": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/children/deploy_hooks",
                },
            },
            {
                "name": "dist",
                "modificationTime": "20160810T172802-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/dist",
                "children": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/children/dist",
                },
            },
            {
                "name": "pip",
                "modificationTime": "20160810T172800-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/pip",
                "children": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/children/pip",
                },
            },
            {
                "name": "teamcity",
                "modificationTime": "20160810T172753-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/teamcity",
                "children": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/children/teamcity",
                },
            },
            {
                "name": "pipdeptree.out.txt",
                "modificationTime": "20160810T172801-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/pipdeptree.out.txt",
                "content": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/content/pipdeptree.out.txt",
                },
            },
            {
                "name": "pipeline_warnings.html",
                "size": 2801,
                "modificationTime": "20160810T172801-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/pipeline_warnings.html",
                "content": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/content/pipeline_warnings.html",
                },
            },
            {
                "name": "requirements.py27.lock",
                "modificationTime": "20160810T172801-0700",
                "href": "/guestAuth/app/rest/builds/id:1216841"
                        "/artifacts/metadata/requirements.py27.lock",
                "content": {
                    "href": "/guestAuth/app/rest/builds/id:1216841"
                            "/artifacts/content/requirements.py27.lock",
                },
            },
        ],
    }
    response_file_metadata_json = {
        "name": "requirements.py27.lock",
        "size": 853,
        "modificationTime": "20160523T163235-0700",
        "href": "/guestAuth/app/rest/builds/id:1216841"
                "/artifacts/metadata/requirements.py27.lock",
        "content": {
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/content/requirements.py27.lock",
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/artifacts/metadata/'),
        json=response_artifacts_metadata_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/artifacts/children/'),
        json=response_artifacts_children_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841'
                        '/artifacts/metadata/requirements.py27.lock'),
        json=response_file_metadata_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841'
                        '/artifacts/metadata/artifact-does-not-exist'),
        status=404,
    )

    deploy_hooks_metadata = {
        "name": "deploy_hooks",
        "modificationTime": "20160523T163236-0700",
        "href": "/guestAuth/app/rest/builds/id:1216841"
                "/artifacts/metadata/deploy_hooks",
        "children": {
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/children/deploy_hooks",
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/'
                        'artifacts/metadata/deploy_hooks'),
        json=deploy_hooks_metadata, status=200,
        content_type='application/json',
    )

    build = tc.builds.all().get(id=1216841)
    assert build.artifacts.isdir()
    assert len(build.artifacts.listdir('*.lock')) == 1
    assert len(build.artifacts.files('*.lock')) == 1
    assert len(build.artifacts.dirs('deploy*')) == 1

    with pytest.raises(exceptions.ArtifactNotFound) as excinfo:
        build.artifacts / 'artifact-does-not-exist'
    assert 'Artifact not found' in str(excinfo.value)

    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/'
                        'artifacts/metadata/artifact_internal_error'),
        status=500,
    )
    with pytest.raises(exceptions.HTTPError) as excinfo:
        build.artifacts / 'artifact_internal_error'

    file_artifact = build.artifacts / 'requirements.py27.lock'
    assert file_artifact.name == 'requirements.py27.lock'
    assert file_artifact.splitext() == ('requirements.py27', '.lock')
    assert file_artifact.ext == '.lock'
    assert file_artifact.fnmatch('*.lock') is True
    assert file_artifact.isfile() is True
    assert 'requirements.py27.lock' in repr(file_artifact)
    assert file_artifact.size == 853
    assert file_artifact.modification_time.year == 2016
    assert file_artifact.modification_time.month == 5
    assert file_artifact.modification_time.day == 23
    assert file_artifact.modification_time.hour == 16
    assert file_artifact.modification_time.minute == 32
    assert file_artifact.modification_time.second == 35

    deploy_hooks = build.artifacts / 'deploy_hooks'
    with pytest.raises(exceptions.IllegalOperation):
        deploy_hooks.content()

    after_deploy_metadata = {
        "name": "after_deploy",
        "size": 237,
        "modificationTime": "20160523T163236-0700",
        "href": "/guestAuth/app/rest/builds/id:1216841"
                "/artifacts/metadata/deploy_hooks/after_deploy",
        "parent": {
            "name": "deploy_hooks",
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/metadata/deploy_hooks",
        },
        "content": {
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/content/deploy_hooks/after_deploy",
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/'
                        'artifacts/metadata/deploy_hooks/after_deploy'),
        json=after_deploy_metadata, status=200,
        content_type='application/json',
    )
    file_artifact = build.artifacts / 'deploy_hooks/after_deploy'
    assert file_artifact.dirname().name == 'deploy_hooks'
    after_deploy_content = """\
#!/bin/sh

echo "*************************************************"
echo
echo "  This is deploy_hooks/after_deploy file running at $0"
echo
echo "*************************************************\n"""
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/'
                        'artifacts/content/deploy_hooks/after_deploy'),
        status=500,
    )
    with pytest.raises(exceptions.HTTPError):
        file_artifact.content()
    responses.reset()
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/'
                        'artifacts/content/deploy_hooks/after_deploy'),
        json=after_deploy_content, status=200,
        content_type='application/json',
    )
    assert b'This is deploy_hooks/after_deploy' in file_artifact.content()


@responses.activate
def test_listdir_failure():
    response_json = {
        "id": 1216841,
        "buildTypeId": "Dummysvc_Branches_Py27",
        "number": "126",
        "href": "/guestAuth/app/rest/builds/id:1216841",
        "artifacts": {
            "href": "/guestAuth/app/rest/builds/id:1216841/"
                    "artifacts/children/",
        },
    }
    response_artifacts_metadata_json = {
        "name": "",
        "modificationTime": "20160810T172802-0700",
        "href": "/guestAuth/app/rest/builds/id:1216841"
                "/artifacts/metadata/",
        "children": {
            "href": "/guestAuth/app/rest/builds/id:1216841"
                    "/artifacts/children/",
        },
    }
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841'),
        json=response_json, status=200,
        content_type='application/json',
    )
    responses.add(
        responses.GET,
        tc.relative_url('app/rest/builds/id:1216841/artifacts/metadata/'),
        json=response_artifacts_metadata_json, status=200,
        content_type='application/json',
    )
    build = tc.builds.all().get(id=1216841)

    with pytest.raises(exceptions.HTTPError):
        responses.add(
            responses.GET,
            tc.relative_url('app/rest/builds/id:1216841/artifacts/children/'),
            status=500,
        )
        build.artifacts.listdir('listdir_failure_*')
