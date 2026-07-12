from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_query_parameters_drive_payload():
    rows = client.get('/prices', params={'ticker': 'MSFT', 'start_date': '2026-02-01', 'end_date': '2026-02-28'}).json()
    assert {row['ticker'] for row in rows} == {'MSFT'}
    assert rows[0]['date'] == '2026-02-01'
    assert rows[-1]['date'] == '2026-02-28'
