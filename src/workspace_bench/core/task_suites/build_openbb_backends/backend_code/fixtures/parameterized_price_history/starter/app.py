from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'historical_prices': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                           'field': 'ticker',
                                                           'headerName': 'Ticker'},
                                                          {'cellDataType': 'text',
                                                           'field': 'date',
                                                           'headerName': 'Date'},
                                                          {'cellDataType': 'text',
                                                           'field': 'close',
                                                           'headerName': 'Close'}]}},
                       'description': 'Historical Prices business data',
                       'endpoint': '/prices',
                       'gridData': {'h': 10, 'w': 20},
                       'name': 'Historical Prices',
                       'params': [{'label': 'Ticker',
                                   'paramName': 'ticker',
                                   'type': 'ticker',
                                   'value': 'AAPL'},
                                  {'label': 'Start',
                                   'paramName': 'start_date',
                                   'type': 'date',
                                   'value': '2026-01-01'},
                                  {'label': 'End',
                                   'paramName': 'end_date',
                                   'type': 'date',
                                   'value': '2026-01-31'}],
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

@app.get('/prices')
def historical_prices(ticker: str = 'AAPL', start_date: str = '', end_date: str = ''):
    return [{'ticker': 'AAPL', 'date': '2026-01-01', 'close': 100.0}]
