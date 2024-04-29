from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models.user import User
from schemas.user import UserCreate, UserInDB

router = APIRouter()


@router.post("/signup", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_create: UserCreate, db: AsyncSession = Depends(get_session)
) -> UserInDB:
    user_dto = jsonable_encoder(user_create)
    user = User(**user_dto)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
