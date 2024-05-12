from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Header, Query
from fastapi.params import Security
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.session_handler import session_handler
from schemas.token import TokenCheckResponse, UserTokenPair
from schemas.user import UserBase
from services.auth_service import AuthService, get_auth_service
from util.JWT_helper import token_check

router = APIRouter()


@router.post(
    "/login",
    response_model=UserTokenPair,
    status_code=HTTPStatus.OK,
    description="Form to login the user in the service and generate the token pair.",
)
async def login(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_agent: Annotated[str | None, Header()] = None,
) -> UserTokenPair:
    user_agent_hash = str(hash(user_agent))
    credentials = UserBase(
        login=form_data.username, password=form_data.password
    )
    tokens = await auth_service.login(
        session=session,
        user=credentials,
        fingerprint=user_agent_hash,
    )
    return tokens


@router.post(
    "/refresh",
    response_model=UserTokenPair,
    status_code=HTTPStatus.OK,
    description="Generate a new token pair.",
)
async def refresh(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    refresh_token: Annotated[str, Body()],
) -> UserTokenPair:
    """Generates the new token pair and returns it to the user."""
    tokens = await auth_service.refresh(
        refresh_token=refresh_token, session=session
    )
    return tokens


@router.post(
    "/logout",
    status_code=HTTPStatus.OK,
    description="Logout the user and delete session.",
)
async def logout(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token_check_data: Annotated[TokenCheckResponse, Security(token_check)],
    logout_everywhere: Annotated[bool, Query()] = False,
) -> dict[str, str]:
    """Logout the user from from service."""
    await auth_service.logout(
        access_token=token_check_data.token,
        session=session,
        logout_everywhere=logout_everywhere,
    )
    return {"status": "User has been successfully logouted."}
