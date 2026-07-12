from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_market_movers_contract():
    widgets = client.get('/widgets.json').json()
    assert 'market_movers' in widgets
    rows = client.get('/movers').json()
    assert len(rows) >= 2
    assert {'symbol', 'change_pct', 'volume'} <= rows[0].keys()
    assert isinstance(rows[0]['volume'], int)
