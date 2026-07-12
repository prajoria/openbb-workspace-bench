from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_existing_status_stays_green():
    assert client.get('/status').json() == {'label': 'API status', 'value': 'operational'}

def test_incident_queue_is_repaired():
    response = client.get('/incidents')
    assert response.status_code == 200
    assert {'incident_id', 'severity', 'owner'} <= response.json()[0].keys()
