from fastapi.routing import APIRoute

from template_fastapi_react.api.routes.health import router as health_router
from template_fastapi_react.main import create_app


def test_app_registers_health_route() -> None:
    app = create_app()
    paths = {
        route.path for route in health_router.routes if isinstance(route, APIRoute)
    }

    assert app.title == "template-fastapi-react"
    assert "" in paths
