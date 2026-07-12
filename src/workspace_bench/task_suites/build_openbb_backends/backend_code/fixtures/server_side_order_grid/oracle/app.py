from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'order_search': {'data': {'dataKey': 'rows',
                           'table': {'columnsDefs': [{'cellDataType': 'text',
                                                      'field': 'order_id',
                                                      'headerName': 'Order ID'},
                                                     {'cellDataType': 'text',
                                                      'field': 'symbol',
                                                      'headerName': 'Symbol'},
                                                     {'cellDataType': 'number',
                                                      'field': 'price',
                                                      'headerName': 'Price'},
                                                     {'cellDataType': 'text',
                                                      'field': 'status',
                                                      'headerName': 'Status'}]}},
                  'description': 'Order Search business data',
                  'endpoint': '/orders/search',
                  'gridData': {'h': 10, 'w': 20},
                  'name': 'Order Search',
                  'type': 'table_ssrm'}}
APPS: list[dict[str, Any]] = []
HEALTH = {'ok': True}

app = FastAPI(title='WorkspaceBench backend')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
def health():
    return HEALTH

@app.get('/widgets.json')
def widgets_json():
    return WIDGETS

ORDERS = [{'order_id': 'O-1', 'price': 185.0, 'status': 'open', 'symbol': 'AAPL'},
 {'order_id': 'O-2', 'price': 420.0, 'status': 'filled', 'symbol': 'MSFT'},
 {'order_id': 'O-3', 'price': 900.0, 'status': 'open', 'symbol': 'NVDA'},
 {'order_id': 'O-4', 'price': 250.0, 'status': 'open', 'symbol': 'TSLA'},
 {'order_id': 'O-5', 'price': 210.0, 'status': 'filled', 'symbol': 'JPM'}]

@app.post('/orders/search')
def order_search(payload: dict):
    rows = list(ORDERS)
    sort_model = payload.get('sortModel') or []
    if sort_model:
        key = sort_model[0].get('colId', 'order_id')
        rows.sort(key=lambda row: str(row.get(key, '')), reverse=sort_model[0].get('sort') == 'desc')
    start = max(int(payload.get('startRow', 0)), 0)
    end = max(int(payload.get('endRow', start + 100)), start)
    page = rows[start:end]
    return {
        'rows': page,
        'totalRows': len(rows),
        'page_size': len(page),
        'first_symbol': page[0]['symbol'] if page else None,
    }
