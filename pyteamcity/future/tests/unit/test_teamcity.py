from pyteamcity.future import TeamCity


def test_username_and_password():
    tc = TeamCity(username='username', password='password')
    assert tc.base_url == 'http://127.0.0.1/httpAuth'
    assert tc.auth == ('username', 'password')


def test_non_standard_http_port():
    tc = TeamCity(protocol='http', port=8000)
    assert tc.base_url == 'http://127.0.0.1:8000/guestAuth'


def test_non_standard_https_port():
    tc = TeamCity(protocol='https', port=8000)
    assert tc.base_url == 'https://127.0.0.1:8000/guestAuth'
