# from typing import Annotated
# from fastapi import APIRouter, Depends, HTTPException
# from app.db.main import get_session
# from sqlmodel.ext.asyncio.session import AsyncSession
# from app.models.users import UserCreate, UserPublic, Token
# from app.services.users import UserService
# from app.api.utils.password_hash import verify_hash
# from app.api.utils.access_token  import generate_token
# from app.api.deps import get_current_user
# from fastapi.security import OAuth2PasswordRequestForm

# router = APIRouter()
# user_service = UserService()

# REFRESH_TOKEN_EXPIRY = 2


# @router.post("/signup", response_model=UserPublic)
# async def create_user(user:UserCreate, session:AsyncSession=Depends(get_session)):
#     new_user = await user_service.create_user(user, session)
#     return new_user


# @router.post("/login/access-token")
# async def login_user(login_data:Annotated[OAuth2PasswordRequestForm, Depends()], session:AsyncSession=Depends(get_session))->Token:
#     username = login_data.username
#     password = login_data.password
#     valid_user = await user_service.read_user_by_username(username, session)
#     if valid_user is not None:
#         valid_password = verify_hash(password=password, hashed_password=valid_user.hashed_password)

#         if valid_password:
#             payload = {
#                 "id": valid_user.id,
#                 "email": valid_user.email,
#                 "username": valid_user.username
#             }
#             access_token = generate_token(  data=payload)

#             return {
#                     "access_token": access_token,
#                     "token_type": "bearer",
#                 }
        
#     raise HTTPException(
#             status_code=401,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#     )


# @router.get("/me", response_model=UserPublic)
# async def get_current_user(current_user:Annotated[UserPublic, Depends(get_current_user)]):
#     return current_user
    

