from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'equity_snapshot': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                         'field': 'symbol',
                                                         'headerName': 'Symbol'},
                                                        {'cellDataType': 'number',
                                                         'field': 'price',
                                                         'headerName': 'Price'},
                                                        {'cellDataType': 'text',
                                                         'field': 'sector',
                                                         'headerName': 'Sector'}]}},
                     'description': 'Equity Snapshot business data',
                     'endpoint': '/equities',
                     'gridData': {'h': 10, 'w': 20},
                     'name': 'Equity Snapshot',
                     'type': 'table'}}
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

@app.get('/equities')
def equities():
    return [{'symbol': 'AAPL', 'price': 201.5, 'sector': 'Technology'}]
