import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from fastapi import status


@pytest.mark.anyio
async def test_health(client: AsyncClient, fastapi_app: FastAPI) -> None:
    """
    Checks the health endpoint.

    :param client: client for the app.
    :param fastapi_app: current FastAPI application.
    """
    url = fastapi_app.url_path_for("health_check")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK


# @pytest.mark.anyio
# async def test_test_end_point_character(client: AsyncClient) -> None:
#     """
#     Test the test endpoint we have.

#     :param client: client for the app.
#     """
#     url = "/api/base-char"
#     response = await client.get(url=url)
#     assert response.status_code == 200