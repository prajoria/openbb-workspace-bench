from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_shared_risk_outputs():
    score = client.get('/risk/score').json()
    note = client.get('/risk/commentary').json()
    assert isinstance(score['value'], float)
    assert 0 < score['value'] < 100
    assert 'risk' in note['markdown'].lower()
    assert len(note['markdown']) > 30
