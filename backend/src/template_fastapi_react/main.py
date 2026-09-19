"""Application factory for the FastAPI backend."""

from fastapi import FastAPI

from template_fastapi_react.api.router import api_router


def create_app() -> FastAPI:
    """Create the FastAPI application."""
    app = FastAPI(title="template-fastapi-react")
    app.include_router(api_router)
    return app


app = create_app()
