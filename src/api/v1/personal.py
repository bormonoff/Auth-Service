from http import HTTPStatus
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres.session_handler import session_handler
from schemas.user import UserSelf, UserSelfResponse
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.post(
    "/register",
    response_model=UserSelfResponse,
    status_code=HTTPStatus.CREATED,
    description="Register a new user.",
)
async def create_user(
    user_service: Annotated[UserService, Depends(get_user_service)],
    db: Annotated[AsyncSession, Depends(session_handler.create_session)],
    user: UserSelf,
) -> UserSelfResponse | HTTPException:
    """Register a user in the authentication service."""
    new_user = await user_service.create_user(db=db, user=user)
    return new_user


@router.get(
    "/personal",
    response_model=UserSelfResponse,
    status_code=HTTPStatus.OK,
    description="Get personal user information.",
)
async def get_current_user_data(
    user_service: Annotated[UserService, Depends(get_user_service)],
    db: Annotated[AsyncSession, Depends(session_handler.create_session)],
    user_id: UUID
) -> UserSelfResponse | HTTPException:
    """Get data about current user."""
    user = await user_service.get_user_from_db(db=db, user=user_id)
    return UserSelfResponse(**user.model_dump())


@router.patch(
    "/personal",
    response_model=UserSelfResponse,
    description="Change personal user information.",
)
async def update_user_data(
    user_service: Annotated[UserService, Depends(get_user_service)],
    db: Annotated[AsyncSession, Depends(session_handler.create_session)],
    user_id: UUID,
    update_user_data: UserSelf,
) -> UserSelfResponse | HTTPException:
    """Change personal user information."""
    updated_user = await user_service.update_user(
        db=db, user=user_id, update_user_data=update_user_data
    )
    return UserSelfResponse(**updated_user.model_dump())


@router.delete("/personal", description="Delete personal data.")
async def delete_user_data(
    user_service: Annotated[UserService, Depends(get_user_service)],
    db: Annotated[AsyncSession, Depends(session_handler.create_session)],
    user_id: UUID
) -> dict[str, str]:
    """Delete personal information."""
    await user_service.delete_user(db=db, user=user_id)
    return {"status": "Data has been successfully deleted."}
