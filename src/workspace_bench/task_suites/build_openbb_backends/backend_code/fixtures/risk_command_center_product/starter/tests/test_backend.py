from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_full_risk_product():
    health = client.get('/health').json()
    assert health['service'] == 'risk-command-center'
    assert health['version'] == '1.0.0'
    widgets = client.get('/widgets.json').json()
    assert set(widgets) == {'risk_overview', 'factor_exposures'}
    app_data = client.get('/apps.json').json()[0]
    assert app_data['name'] == 'Risk Command Center'
    assert isinstance(client.get('/risk/overview').json()['value'], float)
    assert len(client.get('/risk/exposures').json()) >= 2
