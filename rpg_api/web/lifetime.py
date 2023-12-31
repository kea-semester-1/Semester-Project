from collections.abc import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from beanie import init_beanie
from rpg_api.db.postgres.utils import run_scripts
from rpg_api.settings import settings
from rpg_api.db.postgres.meta import meta
from sqlalchemy.sql import text
from rpg_api.db.mongo.models.models import (
    MBaseUser,
    MCharacter,
    MAbility,
    MClass,
    MPlace,
)
from loguru import logger
from neo4j import AsyncGraphDatabase
from motor.motor_asyncio import AsyncIOMotorClient
from rpg_api.web.startup_data_mongo import create_startup_data_mongo

from rpg_api.web.startup_data_pg import create_startup_data_pg
from rpg_api.web.startup_data_neo4j import create_startup_data_Neo4j


async def _setup_pg(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the postgresql database.

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the application's state property.

    :param app: fastAPI application.
    """
    engine = create_async_engine(str(settings.db_url), echo=settings.db_echo)
    session_factory = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext"))

    try:
        await run_scripts(engine)
    except Exception as e:
        logger.info(e)

    await engine.dispose()
    logger.info("Setting up database")


async def _setup_mongodb(app: FastAPI) -> None:  # pragma: no cover
    """
    Creates connection to the mongodb database.

    :param app: fastAPI application.
    """

    client = AsyncIOMotorClient(str(settings.mongodb_url))  # type: ignore

    app.state.mongodb_client = client

    await init_beanie(
        database=client.rpg_api,
        document_models=[
            MBaseUser,
            MCharacter,
            MAbility,
            MClass,
            MPlace,
        ],  # type: ignore
    )

    await create_startup_data_mongo(app)


async def _setup_neo4j(app: FastAPI) -> None:
    """
    Creates a connection to the Neo4j database.

    This function creates a Neo4j driver instance and stores it
    in the application's state property.
    """
    uri = settings.neo_host
    app.state.neo4j_driver = AsyncGraphDatabase.driver(
        uri, auth=(settings.neo_user, settings.neo_pass)
    )
    async with app.state.neo4j_driver.session() as session:
        await create_startup_data_Neo4j(session)


def register_startup_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("startup")
    async def _startup() -> None:  # noqa: WPS430
        app.middleware_stack = None
        await _setup_pg(app)
        await create_startup_data_pg(app)

        await _setup_mongodb(app)
        await _setup_neo4j(app)

        app.middleware_stack = app.build_middleware_stack()

    return _startup


def register_shutdown_event(
    app: FastAPI,
) -> Callable[[], Awaitable[None]]:  # pragma: no cover
    """
    Actions to run on application's shutdown.

    :param app: fastAPI application.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()
        app.state.mongodb_client.close()

    return _shutdown
