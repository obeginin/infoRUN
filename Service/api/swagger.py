from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

"""Swagger"""

def setup_docs(app: FastAPI, get_swagger_user: Depends):
    """
    Настройка Swagger UI и ReDoc с защитой токеном.
    """

    @app.get("/api/docs", dependencies=[Depends(get_swagger_user)])
    async def get_documentation():
        return get_swagger_ui_html(
            openapi_url="/api/openapi.json",
            title="Документация API"
        )

    @app.get("/api/redoc", dependencies=[Depends(get_swagger_user)])
    async def get_redoc_documentation():
        return get_redoc_html(
            openapi_url="/api/openapi.json",
            title="Документация API"
        )

    # openapi.json без защиты
    @app.get("/api/openapi.json")
    async def openapi():
        return app.openapi()

    # Кастомная схема с Bearer токеном
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="Документация API",
            version="1.0.0",
            description="Описание API с авторизацией",
            routes=app.routes,
        )

        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }

        # Добавим схему по умолчанию ко всем методам
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method.setdefault("security", [{"BearerAuth": []}])

        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi