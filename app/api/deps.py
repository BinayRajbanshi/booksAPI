# protecting routes

from fastapi.security import  OAuth2PasswordBearer
from app.core.config import settings
from app.models.users import User, TokenData
from fastapi import Depends, HTTPException, status
from app.api.utils.access_token import verify_token 
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.users import UserService
from typing import Annotated
from jwt.exceptions import InvalidTokenError



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

user_service = UserService()



async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)], session: AsyncSession = Depends(get_session))->User:
    print("returned by the instance", token)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = verify_token(token)
        if not user:
            raise credentials_exception
        validated_token = TokenData(**user)
    except InvalidTokenError:
        raise credentials_exception
    db_user = await session.get(User, validated_token.id)
    if db_user is None:
        raise credentials_exception
    return db_user


# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user