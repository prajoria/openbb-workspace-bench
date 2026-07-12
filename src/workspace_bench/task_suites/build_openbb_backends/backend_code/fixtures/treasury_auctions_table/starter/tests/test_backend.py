from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_auction_contract():
    rows = client.get('/auctions').json()
    assert len(rows) == 2
    assert rows[0]['auction_date'].startswith('2026-')
    assert isinstance(rows[0]['size_billion'], float)
    assert 'Note' in rows[0]['security']
