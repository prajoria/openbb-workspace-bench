from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'research_watchlist': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                            'field': 'symbol',
                                                            'headerName': 'Symbol'},
                                                           {'cellDataType': 'text',
                                                            'field': 'note',
                                                            'headerName': 'Note'}]}},
                        'description': 'Research Watchlist business data',
                        'endpoint': '/watchlist',
                        'gridData': {'h': 10, 'w': 20},
                        'name': 'Research Watchlist',
                        'params': [{'endpoint': '/watchlist/add',
                                    'inputParams': [{'label': 'Symbol',
                                                     'paramName': 'symbol',
                                                     'type': 'text'},
                                                    {'label': 'Note',
                                                     'paramName': 'note',
                                                     'type': 'text'}],
                                    'label': 'Add symbol',
                                    'method': 'POST',
                                    'paramName': 'add_symbol',
                                    'type': 'form'}],
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

WATCHLIST = [{'symbol': 'AAPL', 'note': 'Earnings review'}]

@app.get('/watchlist')
def get_watchlist():
    return WATCHLIST

@app.post('/watchlist/add')
def add_watchlist(payload: dict):
    return {'accepted': True}
