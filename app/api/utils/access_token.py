from datetime import timedelta, datetime, timezone
import jwt 
from app.core.config import settings
import uuid
import logging


def generate_token(data: dict, expires_delta: timedelta | None = None, refresh:bool=False):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    to_encode.update({"jti":str(uuid.uuid4())})
    to_encode.update({"refresh":refresh})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token:str)->dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
        return None


# def generate_token(user_data:dict, expiry:timedelta | None = timedelta(seconds=ACCESS_TOKEN_EXPIRY), refresh:bool=False):
#     payload = {}

#     payload["user"] = user_data
#     payload["exp"] = datetime.now() + expiry
#     payload['jti'] = str(uuid.uuid4())
#     payload['refresh'] = refresh

#     token = jwt.encode(
#         payload=payload,
#         key=settings.JWT_SECRET,
#         algorithm=settings.JWT_ALGORITHM
#     )

#     return token