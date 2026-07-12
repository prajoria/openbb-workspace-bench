from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_cors_and_manifests():
    response = client.get('/widgets.json', headers={'Origin': 'http://localhost'})
    assert response.status_code == 200
    assert response.headers.get('access-control-allow-origin') == '*'

def test_grid_honors_sort_and_page():
    payload = {'startRow': 1, 'endRow': 3, 'sortModel': [{'colId': 'symbol', 'sort': 'desc'}]}
    result = client.post('/orders/search', json=payload).json()
    assert result['totalRows'] == 5
    assert result['page_size'] == 2
    assert result['first_symbol'] == 'NVDA'
    assert [row['symbol'] for row in result['rows']] == ['NVDA', 'MSFT']
