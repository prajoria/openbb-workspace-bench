from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

WIDGETS: dict[str, Any] = {}
APPS: list[dict[str, Any]] = []
HEALTH = {'ok': True, 'service': 'starter'}

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

# Implement the product endpoints described in TASK_BRIEF.md.
