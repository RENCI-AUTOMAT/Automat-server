from starlette.testclient import TestClient
from automat.core import Automat
from automat.server import app
from aioresponses import aioresponses, CallbackResult
import json

client = TestClient(app)


def test_heart_beat():
    response = client.get('/registry')
    assert response.status_code == 200
    assert response.json() == []
    response = client.post('/heartbeat',json= {'host':'some', 'port': '80', 'tag': 'kp1'})
    assert response.status_code == 200
    response = client.get('/registry')
    assert response.status_code == 200
    assert response.json() == ['kp1']


def test_index_path():
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers['content-type'] == 'text/html; charset=utf-8'


def test_open_api_spec():
    response = client.get('/openapi.yml')
    assert response.status_code == 200


def test_unknown_path():
    response = client.get('/non_ex')
    assert response.status_code == 404


def test_proxing_get_to_backend():
    host = 'mock-server'
    port = '80'
    tag = 'mock_server'
    heart_beat_payload = {
        "host": host,
        "port": port,
        "tag": tag
    }
    response = client.post('/heartbeat', json=heart_beat_payload)
    with aioresponses(real_http=True) as mock_server:
        resp = {'proxied': 'value'}
        mock_server.get("http://" + host + ':' + port + '/?', payload=resp)
        resp2 = client.get(f'/{tag}')
        assert resp2.status_code == 200
        assert resp == resp2.json()
        resp2 = client.get(f'/non-existient-kp')
        assert resp2.status_code == 404

def test_proxing_post_to_backend():
    host = 'mock-server'
    port = '80'
    tag = 'mock_server'
    heart_beat_payload = {
        "host": host,
        "port": port,
        "tag": tag
    }
    response = client.post('/heartbeat', json=heart_beat_payload)
    input = {'this is what': 'client sent'}
    output = {'this is what': 'proxied server sent'}

    def assertion_fun(url, **kwargs):
        payload = json.loads(kwargs['data'].decode('utf-8'))
        assert payload == input
        return CallbackResult(status=200, payload=output)

    with aioresponses(real_http=True) as mock_server:
        mock_server.post("http://" + host + ':' + port + '/?', callback=assertion_fun)
        resp2 = client.post(f'/{tag}', json=input)
        assert resp2.status_code == 200
        assert output == resp2.json()

def test_errors_should_be_passed_down_from_proxied():
    host = 'mock-server'
    port = '80'
    tag = 'mock_server'
    heart_beat_payload = {
        "host": host,
        "port": port,
        "tag": tag
    }
    response = client.post('/heartbeat', json=heart_beat_payload)
    input = {'this is what': 'client sent'}
    output = {'this is what': 'proxied server sent'}

    def assertion_fun_412(url, **kwargs):
        payload = json.loads(kwargs['data'].decode('utf-8'))
        assert payload == input
        return CallbackResult(status=412, payload=output)
    def assertion_fun_500(url, **kwargs):
        payload = json.loads(kwargs['data'].decode('utf-8'))
        assert payload == input
        return CallbackResult(status=500, payload=output)

    with aioresponses(real_http=True) as mock_server:
        mock_server.post("http://" + host + ':' + port + '/?', callback=assertion_fun_412)
        mock_server.post("http://" + host + ':' + port + '/another_endpoint?', callback=assertion_fun_500)

        resp2 = client.post(f'/{tag}', json=input)
        resp3 = client.post(f'/{tag}/another_endpoint', json=input)
        assert resp2.status_code == 412
        assert output == resp2.json()
        assert resp3.status_code == 500
        assert  output == resp3.json()