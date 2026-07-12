from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_submission_mutates_watchlist():
    response = client.post('/watchlist/add', json={'symbol': 'tsla', 'note': 'Delivery watch'})
    assert response.status_code == 200
    rows = client.get('/watchlist').json()
    assert {'symbol': 'TSLA', 'note': 'Delivery watch'} in rows
