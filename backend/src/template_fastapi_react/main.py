"""Application factory for the FastAPI backend."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from template_fastapi_react.api.router import api_router


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(title="template-fastapi-react")
    app.include_router(api_router)
    static_dir = Path("/app/static")
    if static_dir.is_dir():
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")
    return app


app = create_app()
