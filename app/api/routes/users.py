from typing import List
from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.users import UserCreate, UserPublic, UserUpdate
from app.services.users import UserService

router = APIRouter()
user_service = UserService()

@router.post("/signup", response_model=UserPublic)
async def create_user(user:UserCreate, session:AsyncSession=Depends(get_session)):
    new_user = await user_service.create_user(user, session)
    return new_user


@router.get("/users/{id}", response_model=UserPublic)
async def get_user(id:int, session:AsyncSession = Depends(get_session)):
    user = await user_service.read_user(id, session)
    return user


@router.get("/users",response_model=List[UserPublic])
async def read_users(limit:int=Query(default=20, le=100), offset:int=0,session:AsyncSession=Depends(get_session)):
    users = await user_service.read_users(limit=limit, offset=offset, session=session)
    return users