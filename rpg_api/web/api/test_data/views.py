from rpg_api import exceptions
from rpg_api.services.email_service.email_dependencies import GetEmailService
from rpg_api.utils import dtos
from rpg_api.web.api.postgres.auth import auth_utils as utils
from rpg_api.web.api.postgres.auth.token_store import token_store
from fastapi.routing import APIRouter
from rpg_api.utils.daos import GetDAOs
from rpg_api.settings import settings
from pydantic import BaseModel
from rpg_api.db.postgres.factory import factories

router = APIRouter()


class GenerateTestDataDTO(BaseModel):
    amount: int


@router.post("/generate-test-data", status_code=201)
async def generate_test_data(
    input_dto: GenerateTestDataDTO,
    daos: GetDAOs,
) -> dtos.EmptyDefaultResponse:
    """Generate test data."""

    factories.AsyncFactory.session = daos.session

    base_class = await factories.BaseClassFactory.create()
    for _ in range(input_dto.amount):
        try:
            user = await factories.BaseUserFactory.create()
            for _ in range(10):
                character = await factories.CharacterFactory.create(
                    user=user, base_class=base_class
                )
        except Exception as e:
            print(e)

    return dtos.EmptyDefaultResponse()
