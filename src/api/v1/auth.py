from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.session_handler import session_handler
from schemas.token import UserTokenPair
from schemas.user import UserBase
from services.auth_service import AuthService, get_token_service

router = APIRouter()


@router.post(
    "/login",
    response_model=UserTokenPair,
    status_code=HTTPStatus.OK,
    description="Login the user in the service and generate the token pair.",
)
async def login(
    user: UserBase,
    fingerprint: str,
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    token_service: Annotated[AuthService, Depends(get_token_service)]
) -> UserTokenPair | HTTPException:
    """Creates tokens when the user login and returns them to the user."""
    tokens = await token_service.login(user=user, session=session, fingerprint=fingerprint)
    return tokens


@router.post(
    "/refresh",
    response_model=UserTokenPair,
    status_code=HTTPStatus.OK,
    description="Generate a new token pair.",
)
async def refresh(
    token: str,
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    token_service: Annotated[AuthService, Depends(get_token_service)]
) -> UserTokenPair | HTTPException:
    """Generates the new token pair and returns it to the user."""
    tokens = await token_service.refresh(token=token, session=session)
    return tokens


@router.post(
    "/logout",
    status_code=HTTPStatus.OK,
    description="Logout the user and delete session.",
)
async def logout(
    token: str,
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    token_service: Annotated[AuthService, Depends(get_token_service)]
) -> dict[str, str]:
    """Logout the user from from service."""
    await token_service.logout(token=token, session=session)
    return {"status": "User has been successfully logouted."}