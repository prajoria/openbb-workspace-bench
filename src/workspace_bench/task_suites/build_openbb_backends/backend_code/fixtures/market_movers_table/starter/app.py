from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'market_movers': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                       'field': 'symbol',
                                                       'headerName': 'Symbol'},
                                                      {'cellDataType': 'text',
                                                       'field': 'change_pct',
                                                       'headerName': 'Change %'},
                                                      {'cellDataType': 'number',
                                                       'field': 'volume',
                                                       'headerName': 'Volume'}]}},
                   'description': 'Market Movers business data',
                   'endpoint': '/movers',
                   'gridData': {'h': 10, 'w': 20},
                   'name': 'Market Movers',
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

@app.get('/movers')
def market_movers():
    return [{'symbol': 'TODO', 'change_pct': None, 'volume': None}]
