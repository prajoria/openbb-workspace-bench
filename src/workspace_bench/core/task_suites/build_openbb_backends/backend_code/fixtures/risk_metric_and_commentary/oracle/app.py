from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from analytics import risk_summary

WIDGETS: dict[str, Any] = {'risk_commentary': {'description': 'Risk Commentary business data',
                     'endpoint': '/risk/commentary',
                     'gridData': {'h': 10, 'w': 20},
                     'name': 'Risk Commentary',
                     'type': 'markdown'},
 'risk_score': {'description': 'Portfolio Risk Score business data',
                'endpoint': '/risk/score',
                'gridData': {'h': 10, 'w': 20},
                'name': 'Portfolio Risk Score',
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

@app.get('/risk/score')
def risk_score():
    return {'label': 'Portfolio risk', 'value': risk_summary()['score'], 'unit': '/100'}

@app.get('/risk/commentary')
def risk_commentary():
    return {'markdown': risk_summary()['commentary']}
