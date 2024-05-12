from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Body, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import get_settings
from db.postgres.session_handler import session_handler
from schemas.role import (
    RoleCreateSchema,
    RoleResponseSchema,
    RoleTitleSchema,
    RoleUpdateSchema,
)
from services.role_service import RoleService, get_role_service

router = APIRouter()


@router.get(
    "/",
    response_model=list[RoleResponseSchema],
    description="Get the list of the roles",
    status_code=HTTPStatus.OK,
)
async def get_all_roles(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
) -> list[RoleResponseSchema]:
    roles = await role_service.list(session=session)
    return roles


@router.post(
    "/",
    response_model=RoleResponseSchema,
    description="Create a role.",
    status_code=HTTPStatus.CREATED,
)
async def create_role(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    role: RoleCreateSchema = Body(
        description="Spectify 'title' and 'description' of new role"
    ),
) -> RoleResponseSchema:
    """Create a new role."""
    result = await role_service.create(session=session, role=role)
    return result


@router.get(
    "/{role_title}",
    response_model=RoleResponseSchema,
    description="Get all infomation about a role.",
    status_code=HTTPStatus.OK,
)
async def get_role(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    role_title: str = Path(
        description="Role title. Letters and digits only. 3-50 characters long.",
        pattern=get_settings().ROLE_TITLE_PATTERN,
    ),
) -> RoleResponseSchema:
    """Get a role information."""
    role = RoleTitleSchema(title=role_title)
    result = await role_service.get(session=session, role=role)
    return result


@router.patch(
    "/{role_title}",
    response_model=RoleResponseSchema,
    description="Update information about a role.",
    status_code=HTTPStatus.OK,
)
async def update_role(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    role_title: str = Path(
        description="Role title. Letters and digits only. 3-50 characters long.",
        pattern=get_settings().ROLE_TITLE_PATTERN,
    ),
    update_role_data: RoleUpdateSchema = Body(
        description="Spectify new values for field 'title' or(and) 'description'"
    ),
) -> RoleResponseSchema:
    """Update information about a role."""
    role_title_obj = RoleTitleSchema(title=role_title)
    result = await role_service.update(
        session=session,
        role_title=role_title_obj,
        update_role_data=update_role_data,
    )
    return result


@router.delete(
    "/{role_title}",
    response_model=None,
    description="Delete infromation about a role.",
    status_code=HTTPStatus.OK,
)
async def delete_role(
    session: Annotated[AsyncSession, Depends(session_handler.create_session)],
    role_service: Annotated[RoleService, Depends(get_role_service)],
    role_title: str = Path(
        description="Role title. Letters and digits only. 3-50 characters long.",
        pattern=get_settings().ROLE_TITLE_PATTERN,
    ),
) -> dict[str, str]:
    """Delete infromation about a role."""
    role_title_obj = RoleTitleSchema(title=role_title)
    await role_service.delete(session=session, role=role_title_obj)
    return {"status": f"Role {role_title} has been successfully deleted."}
