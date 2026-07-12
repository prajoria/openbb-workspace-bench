from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_manifest_columns_exist_in_payload():
    widget = client.get('/widgets.json').json()['client_trades']
    fields = {item['field'] for item in widget['data']['table']['columnsDefs']}
    rows = client.get('/client-trades').json()
    assert fields == {'client_name', 'notional', 'side'}
    assert all(fields <= row.keys() for row in rows)
