from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'incident_queue': {'data': {'table': {'columnsDefs': [{'cellDataType': 'text',
                                                        'field': 'incident_id',
                                                        'headerName': 'Incident'},
                                                       {'cellDataType': 'text',
                                                        'field': 'severity',
                                                        'headerName': 'Severity'},
                                                       {'cellDataType': 'text',
                                                        'field': 'owner',
                                                        'headerName': 'Owner'}]}},
                    'description': 'Incident Queue business data',
                    'endpoint': '/incidents',
                    'gridData': {'h': 10, 'w': 20},
                    'name': 'Incident Queue',
                    'type': 'table'},
 'service_status': {'description': 'Service Status business data',
                    'endpoint': '/status',
                    'gridData': {'h': 10, 'w': 20},
                    'name': 'Service Status',
                    'type': 'metric'}}
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

@app.get('/status')
def service_status():
    return {'label': 'API status', 'value': 'operational'}

@app.get('/incidents')
def incidents():
    return [
        {'incident_id': 'INC-104', 'severity': 'high', 'owner': 'platform'},
        {'incident_id': 'INC-105', 'severity': 'medium', 'owner': 'data'},
    ]
