from fastapi import FastAPI, Depends, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from Service.Crud.auth import get_swagger_user
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

"""Swagger"""
swagger_router = APIRouter()
security = HTTPBasic()





# Обработка остальных маршрутов (если SPA)
'''@app.get("/{full_path:path}")
def read_spa(full_path: str):
    excluded_paths = ("api", "docs", "openapi.json", "redoc")
    if any(full_path == p or full_path.startswith(p + "/") for p in excluded_paths):
        raise HTTPException(status_code=404)
    return FileResponse(os.path.join(frontend_path, "index.html"))'''

