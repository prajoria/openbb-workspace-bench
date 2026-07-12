from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'client_trades': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                       'field': 'client_name',
                                                       'headerName': 'Client'},
                                                      {'cellDataType': 'number',
                                                       'field': 'notional',
                                                       'headerName': 'Notional'},
                                                      {'cellDataType': 'text',
                                                       'field': 'side',
                                                       'headerName': 'Side'}]}},
                   'description': 'Client Trades business data',
                   'endpoint': '/client-trades',
                   'gridData': {'h': 10, 'w': 20},
                   'name': 'Client Trades',
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

@app.get('/client-trades')
def client_trades():
    return [{'customer': 'Northstar Fund', 'amount': 2500000, 'direction': 'buy'}]
