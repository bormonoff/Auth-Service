from http import HTTPStatus

import pytest
from settings import get_settings
from testdata.personal import NEW_USER_DATA, SUPERUSER_DATA

pytestmark = pytest.mark.profile

ENDPOINT = f"{get_settings().API_URL}/profile/personal"


@pytest.mark.asyncio
async def test_get_user(
    prepare_users, prepare_headers_with_superuser_token, get_http_session
):
    """Checks can we get a user via a token."""
    response = await get_http_session.get(
        url=ENDPOINT, headers=prepare_headers_with_superuser_token
    )
    body = await response.json()
    status = response.status

    assert status == HTTPStatus.OK
    assert body["login"] == SUPERUSER_DATA["login"]
    assert body["email"] == SUPERUSER_DATA["email"]
    assert body["first_name"] == SUPERUSER_DATA["first_name"]
    assert body["last_name"] == SUPERUSER_DATA["last_name"]


@pytest.mark.asyncio
async def test_change_user(
    prepare_users, prepare_headers_with_superuser_token, get_http_session
):
    """Checks can we change a user data via a token."""
    response = await get_http_session.patch(
        url=ENDPOINT,
        headers=prepare_headers_with_superuser_token,
        json=NEW_USER_DATA,
    )
    body = await response.json()
    status = response.status

    assert status == HTTPStatus.OK
    assert body["login"] == NEW_USER_DATA["login"]
    assert body["email"] == NEW_USER_DATA["email"]
    assert body["first_name"] == NEW_USER_DATA["first_name"]
    assert body["last_name"] == NEW_USER_DATA["last_name"]


@pytest.mark.asyncio
async def test_delete_user(
    prepare_users, prepare_headers_with_superuser_token, get_http_session
):
    """Checks can we delete a user data via a token."""
    response = await get_http_session.delete(
        url=ENDPOINT,
        headers=prepare_headers_with_superuser_token,
        json=NEW_USER_DATA,
    )
    status = response.status

    assert status == HTTPStatus.OK
