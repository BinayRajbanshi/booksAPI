from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.users import UserCreate, UserPublic, UserUpdate, UserLogin
from app.services.users import UserService
from app.api.utils.password_hash import verify_hash
from app.api.utils.access_token  import generate_token, verify_token
from datetime import timedelta
from app.api.deps import AccessTokenBearer

router = APIRouter()
user_service = UserService()
access_token_bearer = AccessTokenBearer()

REFRESH_TOKEN_EXPIRY = 2


@router.post("/signup", response_model=UserPublic)
async def create_user(user:UserCreate, session:AsyncSession=Depends(get_session)):
    new_user = await user_service.create_user(user, session)
    return new_user


@router.post("/login")
async def login_user(login_data:UserLogin, session:AsyncSession=Depends(get_session)):
    email = login_data.email
    password = login_data.password
    valid_user = await user_service.read_user_by_email(email, session)
    if valid_user is not None:
        valid_password = verify_hash(password=password, hashed_password=valid_user.hashed_password)

        if valid_password:
            payload = {
                "id": valid_user.id,
                "email": valid_user.email,
                # "first_name": user.first
            }
            access_token = generate_token(user_data=payload)
            refresh_token = generate_token(user_data=payload, expiry=timedelta(days=REFRESH_TOKEN_EXPIRY), refresh=True)

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"id": valid_user.id, "email": valid_user.email},
                }
            )
    raise HTTPException(status_code=401, detail="Please check your email or password")


@router.get("/users/{id}", response_model=UserPublic)
async def read_user(id:int, session:AsyncSession = Depends(get_session)):
    user = await user_service.read_user(id, session)
    return user


@router.get("/users",response_model=List[UserPublic])
async def read_users(limit:int=Query(default=20, le=100), offset:int=0,session:AsyncSession=Depends(get_session), user_details=Depends(access_token_bearer)):
    users = await user_service.read_users(limit=limit, offset=offset, session=session)
    return users


@router.delete("/users/{id}", response_model=UserPublic)
async def delete_user(id:int, session:AsyncSession = Depends(get_session) ):
    deleted_user = await user_service.delete_user(id, session)
    return deleted_user