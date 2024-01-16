from fastapi.routing import APIRouter

from rpg_api.web.api.postgres.router import pg_router
from rpg_api.web.api.neo4j.router import neo4j_router
from rpg_api.web.api.monitoring import monitoring_router
from rpg_api.web.api.test_data.views import router as test_data_router

from rpg_api.web.api.mongo.router import mongo_router


api_router = APIRouter()

api_router.include_router(pg_router, prefix="/postgres", tags=["postgres"])
api_router.include_router(neo4j_router, prefix="/neo4j", tags=["neo4j"])
api_router.include_router(mongo_router, prefix="/mongodb", tags=["mongodb"])

api_router.include_router(monitoring_router, prefix="/monitoring", tags=["monitoring"])
api_router.include_router(test_data_router, prefix="/test-data", tags=["test-data"])
