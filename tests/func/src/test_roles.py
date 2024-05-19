from http import HTTPStatus

import pytest
from settings import get_settings
from testdata.common import HEADERS
from testdata.roles import (
    CREATE_ROLE,
    DELETE_ROLE,
    GET_ROLE,
    INVALID_ROLE,
    UPDATE_ROLE,
)

pytestmark = pytest.mark.roles

ENDPOINT = f"{get_settings().API_URL}/roles"


@pytest.mark.asyncio
@pytest.mark.parametrize("role", CREATE_ROLE)
async def test_create_role(
    empty_db_tables,
    prepare_headers_with_superuser_token,
    get_http_session,
    role,
):
    """Checks that a role API sucessfully creates a role."""
    response = await get_http_session.post(
        url=ENDPOINT, headers=prepare_headers_with_superuser_token, json=role
    )
    body = await response.json()

    assert response.status == HTTPStatus.CREATED
    assert body["title"] == role["title"]
    assert body["description"] == role["description"]


@pytest.mark.asyncio
async def test_create_role_with_invalid_role_title(
    empty_db_tables, get_http_session
):
    """Checks that a role API can't create a role with invalid creds."""
    response = await get_http_session.post(
        url=ENDPOINT, headers=HEADERS, json=INVALID_ROLE
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_role_unique(empty_db_tables, get_http_session):
    """Checks that a role API can't create non unique role."""
    for _ in range(2):
        response = await get_http_session.post(
            url=ENDPOINT, headers=HEADERS, json=CREATE_ROLE[0]
        )
    body = await response.json()

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert body["detail"] == "DB Error - already exists. "


@pytest.mark.asyncio
@pytest.mark.parametrize("role", GET_ROLE)
async def test_get_role(
    empty_db_tables, prepare_roles, get_http_session, role
):
    """Checks that a role API returns a proper role."""
    url = f"{ENDPOINT}/{role['role_title']}"

    response = await get_http_session.get(url=url, headers=HEADERS)

    assert response.status == role["result"]


@pytest.mark.asyncio
@pytest.mark.parametrize("role", DELETE_ROLE)
async def test_delete_role(
    empty_db_tables, prepare_roles, get_http_session, role
):
    """Checks that a role API sucessfully deletes a proper role."""
    url = f"{ENDPOINT}/{role['role_title']}"

    response = await get_http_session.delete(url=url, headers=HEADERS)

    assert response.status == role["result"]


@pytest.mark.asyncio
@pytest.mark.parametrize("role", UPDATE_ROLE)
async def test_update_role(
    empty_db_tables, prepare_roles, get_http_session, role
):
    """Checks that a role API sucessfully updates a proper role."""
    url = f"{ENDPOINT}/{role['role_title']}"

    response = await get_http_session.patch(
        url=url, headers=HEADERS, json=role["update_data"]
    )

    assert response.status == role["result"]["status"]
    if role["result"]["status"] == HTTPStatus.OK:
        body = await response.json()
        assert body == role["result"]["body"]
