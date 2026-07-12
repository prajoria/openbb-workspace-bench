from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_existing_equity_domain_is_unchanged():
    assert client.get('/equities').json() == [{'symbol': 'AAPL', 'price': 201.5, 'sector': 'Technology'}]

def test_credit_domain_is_added():
    widgets = client.get('/widgets.json').json()
    assert {'equity_snapshot', 'credit_spreads'} <= widgets.keys()
    rows = client.get('/credit-spreads').json()
    assert len(rows) >= 2
    assert {'issuer', 'rating', 'spread_bps'} <= rows[0].keys()
