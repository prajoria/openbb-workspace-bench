from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'credit_spreads': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                        'field': 'issuer',
                                                        'headerName': 'Issuer'},
                                                       {'cellDataType': 'text',
                                                        'field': 'rating',
                                                        'headerName': 'Rating'},
                                                       {'cellDataType': 'text',
                                                        'field': 'spread_bps',
                                                        'headerName': 'Spread bps'}]}},
                    'description': 'Credit Spreads business data',
                    'endpoint': '/credit-spreads',
                    'gridData': {'h': 10, 'w': 20},
                    'name': 'Credit Spreads',
                    'type': 'table'},
 'equity_snapshot': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
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

@app.get('/credit-spreads')
def credit_spreads():
    return [
        {'issuer': 'Acme Industrial', 'rating': 'BBB', 'spread_bps': 142},
        {'issuer': 'Northstar Bank', 'rating': 'A', 'spread_bps': 88},
    ]
