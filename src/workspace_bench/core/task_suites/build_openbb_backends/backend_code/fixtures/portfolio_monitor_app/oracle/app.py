from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'portfolio_positions': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                             'field': 'symbol',
                                                             'headerName': 'Symbol'},
                                                            {'cellDataType': 'text',
                                                             'field': 'weight',
                                                             'headerName': 'Weight'},
                                                            {'cellDataType': 'text',
                                                             'field': 'market_value',
                                                             'headerName': 'Market Value'}]}},
                         'description': 'Portfolio Positions business data',
                         'endpoint': '/portfolio/positions',
                         'gridData': {'h': 10, 'w': 20},
                         'name': 'Portfolio Positions',
                         'type': 'table'},
 'portfolio_summary': {'description': 'Portfolio Summary business data',
                       'endpoint': '/portfolio/summary',
                       'gridData': {'h': 10, 'w': 20},
                       'name': 'Portfolio Summary',
                       'type': 'metric'}}
APPS: list[dict[str, Any]] = [{'description': 'Portfolio Monitor application',
  'name': 'Portfolio Monitor',
  'tabs': {'main': {'id': 'main',
                    'layout': [{'h': 10, 'i': 'portfolio_summary', 'w': 20, 'x': 0, 'y': 0},
                               {'h': 10, 'i': 'portfolio_positions', 'w': 20, 'x': 20, 'y': 0}],
                    'name': 'Overview'}},
  'template_id': 'portfolio-monitor'}]
HEALTH = {'ok': True}

app = FastAPI(title='WorkspaceBench backend')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'], allow_headers=['*'])

@app.get('/health')
def health():
    return HEALTH

@app.get('/widgets.json')
def widgets_json():
    return WIDGETS

@app.get('/apps.json')
def apps_json():
    return APPS

@app.get('/portfolio/summary')
def portfolio_summary():
    return {'label': 'Portfolio value', 'value': 1250000, 'currency': 'USD'}

@app.get('/portfolio/positions')
def portfolio_positions():
    return [
        {'symbol': 'AAPL', 'weight': 0.32, 'market_value': 400000},
        {'symbol': 'MSFT', 'weight': 0.28, 'market_value': 350000},
    ]
