from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.session_handler import session_handler
from schemas.token import TokenPair
from schemas.user import UserBase
from services.token_service import TokenService, get_token_service

router = APIRouter()


@router.post(
    "/login",
    response_model=TokenPair,
    status_code=HTTPStatus.ACCEPTED,
    description="Login a user in the service.",
)
async def login(
    user: UserBase,
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    token_service: Annotated[TokenService, Depends(get_token_service)]
) -> TokenPair | HTTPException:
    """Create tokens when a user login."""
    tokens = await token_service.login(user=user, session=session)
    return tokens