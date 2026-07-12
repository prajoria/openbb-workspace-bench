from typing import Any

from fastapi import FastAPI, HTTPException

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
    raise HTTPException(status_code=500, detail='database mapping failed')
