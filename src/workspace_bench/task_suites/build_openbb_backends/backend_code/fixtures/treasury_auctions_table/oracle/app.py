from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'auction_calendar': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                          'field': 'auction_date',
                                                          'headerName': 'Auction Date'},
                                                         {'cellDataType': 'text',
                                                          'field': 'security',
                                                          'headerName': 'Security'},
                                                         {'cellDataType': 'number',
                                                          'field': 'size_billion',
                                                          'headerName': 'Size ($bn)'}]}},
                      'description': 'Treasury Auction Calendar business data',
                      'endpoint': '/auctions',
                      'gridData': {'h': 10, 'w': 20},
                      'name': 'Treasury Auction Calendar',
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

@app.get('/auctions')
def auction_calendar():
    return [
        {'auction_date': '2026-08-11', 'security': '3-Year Note', 'size_billion': 58.0},
        {'auction_date': '2026-08-12', 'security': '10-Year Note', 'size_billion': 42.0},
    ]
