from importlib import metadata

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from rpg_api.logging import configure_logging
from rpg_api.web.api.router import api_router
from rpg_api.web.lifetime import register_shutdown_event, register_startup_event

from rpg_api.web.api.websockets.router import websocket_router


def get_app() -> FastAPI:
    """
    Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    configure_logging()
    app = FastAPI(
        title="rpg_api",
        version=metadata.version("rpg_api"),
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Adds startup and shutdown events.
    register_startup_event(app)
    register_shutdown_event(app)

    # Main router for the API.
    app.include_router(router=api_router, prefix="/api")
    app.include_router(websocket_router)

    return app
