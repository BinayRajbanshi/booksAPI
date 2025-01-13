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


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
    scheme_name="access_token"
)

class TokenVerifier():
    def __init__(self, token_type:str):
        self.token_type = token_type
    
    async def __call__(self, token:str = Depends(oauth2_scheme)):
        if not token:
            raise credentials_exception
   
        token_data = verify_token(token)
        if token_data is not None:
            print(f"returned token {token_data}")
            validated_token = TokenData(**token_data)
        else:
            raise credentials_exception
        
        self.verify_token_type(validated_token)
        return validated_token
    
    def verify_token_type(self, token_data: TokenData):
        is_refresh = token_data.refresh == True
        if self.token_type == "refresh" and not is_refresh:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token"
            )
        elif self.token_type=="access" and is_refresh:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid access token"
            )
            

access_token_verifier = TokenVerifier("access")
refresh_token_verifier = TokenVerifier("refresh")

user_service = UserService()


# DEPENDENCY CHAIN TO RETRIVE THE TOKEN AND THEN VERIFY THE TOKEN
async def get_current_user(
    token_data: Annotated[TokenData, Depends(access_token_verifier)],
    session: Annotated[AsyncSession, Depends(get_session)]
) -> User:
    db_user = await session.get(User, token_data.id)
    if db_user is None:
        raise credentials_exception
    return db_user





# async def get_current_active_user(
#     current_user: Annotated[User, Depends(get_current_user)],
# ):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user