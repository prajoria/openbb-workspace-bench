from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_chart_series_are_constructable():
    rows = client.get('/revenue-trend').json()
    assert len(rows) >= 3
    assert all({'quarter', 'revenue', 'operating_margin'} <= row.keys() for row in rows)
    assert all(isinstance(row['revenue'], float) for row in rows)
