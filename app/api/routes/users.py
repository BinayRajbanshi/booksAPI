from typing import List, Annotated
from fastapi import APIRouter, Depends, Query, HTTPException
from pydantic import EmailStr
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.users import UserCreate, UserPublic, Token,User
from app.services.users import UserService
from app.api.utils.password_hash import verify_hash
from app.api.utils.access_token  import generate_token, verify_token
from datetime import timedelta
from app.api.deps import get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2


@router.post("/signup", response_model=UserPublic )
async def create_user(user:UserCreate, session:AsyncSession=Depends(get_session)):
    new_user = await user_service.create_user(user, session)
    return new_user


@router.post("/login/access-token")
async def login_user(login_data:Annotated[OAuth2PasswordRequestForm, Depends()], session:AsyncSession=Depends(get_session))->Token:
    username = login_data.username
    password = login_data.password
    valid_user = await user_service.read_user_by_username(username, session)
    if valid_user is not None:
        valid_password = verify_hash(password=password, hashed_password=valid_user.hashed_password)

        if valid_password:
            payload = {
                "id": valid_user.id,
                "email": valid_user.email,
                "username": valid_user.username
            }
            access_token = generate_token(  data=payload)

            return {
                    "access_token": access_token,
                    "token_type": "bearer",
                }
        
    raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/users/me", response_model=UserPublic)
async def read_current_user(current_user:Annotated[User, Depends(get_current_user)]):
    return current_user
    


@router.get("/users/{id}", response_model=UserPublic)
async def read_user(id:int, session:AsyncSession = Depends(get_session)):
    user = await user_service.read_user(id, session)
    return user


@router.get("/users",response_model=List[UserPublic])
async def read_users(limit:int=Query(default=20, le=100), offset:int=0,session:AsyncSession=Depends(get_session)):
    users = await user_service.read_users(limit=limit, offset=offset, session=session)
    return users


@router.delete("/users/{id}", response_model=UserPublic)
async def delete_user(id:int, session:AsyncSession = Depends(get_session) ):
    deleted_user = await user_service.delete_user(id, session)
    return deleted_user