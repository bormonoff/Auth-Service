from http import HTTPStatus

import pytest

from settings import get_settings
from testdata.common import HEADERS
from testdata.personal import USER_DATA, INVALID_USER_LOGIN_DATA, INVALID_USER_NAME, INVALID_USER_SURNAME

pytestmark = pytest.mark.profile

ENDPOINT = f"{get_settings().API_URL}/profile/register"


@pytest.mark.asyncio
@pytest.mark.parametrize("user", USER_DATA)
async def test_success_registration(empty_db_tables, get_http_session, user):
    """Checks user registration."""
    response = await get_http_session.post(url=ENDPOINT, headers=HEADERS, json=user)
    body = await response.json()
    status = response.status

    assert status == HTTPStatus.CREATED
    assert body["login"] == user["login"]
    assert body["email"] == user["email"]
    assert body["first_name"] == user["first_name"]
    assert body["last_name"] == user["last_name"]


@pytest.mark.asyncio
@pytest.mark.parametrize("user", INVALID_USER_LOGIN_DATA)
async def test_wrong_login_registration(empty_db_tables, get_http_session, user):
    """Checks invalid registration with incorrect login."""
    response = await get_http_session.post(url=ENDPOINT, headers=HEADERS, json=INVALID_USER_NAME)
    status = response.status

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_wrong_name_registration(empty_db_tables, get_http_session):
    """Checks invalid registration with incorrect name."""
    response = await get_http_session.post(url=ENDPOINT, headers=HEADERS, json=INVALID_USER_NAME)
    status = response.status

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_wrong_name_registration(empty_db_tables, get_http_session):
    """Checks invalid registration with incorrect surname."""
    response = await get_http_session.post(url=ENDPOINT, headers=HEADERS, json=INVALID_USER_SURNAME)
    status = response.status

    assert status == HTTPStatus.UNPROCESSABLE_ENTITY