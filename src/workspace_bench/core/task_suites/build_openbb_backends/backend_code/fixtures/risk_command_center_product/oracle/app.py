from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'factor_exposures': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                          'field': 'factor',
                                                          'headerName': 'Factor'},
                                                         {'cellDataType': 'text',
                                                          'field': 'exposure',
                                                          'headerName': 'Exposure'},
                                                         {'cellDataType': 'text',
                                                          'field': 'limit',
                                                          'headerName': 'Limit'}]}},
                      'description': 'Factor Exposures business data',
                      'endpoint': '/risk/exposures',
                      'gridData': {'h': 10, 'w': 20},
                      'name': 'Factor Exposures',
                      'type': 'table'},
 'risk_overview': {'description': 'Risk Overview business data',
                   'endpoint': '/risk/overview',
                   'gridData': {'h': 10, 'w': 20},
                   'name': 'Risk Overview',
                   'type': 'metric'}}
APPS: list[dict[str, Any]] = [{'description': 'Risk Command Center application',
  'name': 'Risk Command Center',
  'tabs': {'main': {'id': 'main',
                    'layout': [{'h': 10, 'i': 'risk_overview', 'w': 20, 'x': 0, 'y': 0},
                               {'h': 10, 'i': 'factor_exposures', 'w': 20, 'x': 20, 'y': 0}],
                    'name': 'Overview'}},
  'template_id': 'risk-command-center'}]
HEALTH = {'ok': True, 'service': 'risk-command-center', 'version': '1.0.0'}

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

@app.get('/risk/overview')
def risk_overview():
    return {'label': 'Risk utilization', 'value': 63.4, 'status': 'within limit'}

@app.get('/risk/exposures')
def risk_exposures():
    return [
        {'factor': 'Technology', 'exposure': 0.28, 'limit': 0.35},
        {'factor': 'Rates duration', 'exposure': 4.2, 'limit': 6.0},
    ]
