from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {'revenue_trend': {'data': {'categoryField': 'quarter',
                            'series': [{'field': 'revenue'}, {'field': 'operating_margin'}]},
                   'description': 'Revenue and Margin Trend business data',
                   'endpoint': '/revenue-trend',
                   'gridData': {'h': 10, 'w': 20},
                   'name': 'Revenue and Margin Trend',
                   'type': 'chart'}}
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

@app.get('/revenue-trend')
def revenue_trend():
    return [
        {'quarter': 'Q1 2026', 'revenue': 12.4, 'operating_margin': 18.2},
        {'quarter': 'Q2 2026', 'revenue': 13.1, 'operating_margin': 19.0},
        {'quarter': 'Q3 2026', 'revenue': 14.0, 'operating_margin': 20.1},
    ]
