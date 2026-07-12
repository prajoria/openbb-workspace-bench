from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_app_references_served_widgets():
    widgets = client.get('/widgets.json').json()
    app_data = client.get('/apps.json').json()[0]
    refs = {item['i'] for item in app_data['tabs']['main']['layout']}
    assert refs == set(widgets)
    assert isinstance(client.get('/portfolio/summary').json()['value'], int)
    assert client.get('/portfolio/positions').json()[0]['symbol'] == 'AAPL'
