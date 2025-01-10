from datetime import timedelta, datetime
import jwt 
from app.core.config import settings
import uuid
import logging


ACCESS_TOKEN_EXPIRY = 3600 # one hour for expiring the token


def generate_token(user_data:dict, expiry:timedelta = timedelta(seconds=ACCESS_TOKEN_EXPIRY), refresh:bool=False):
    payload = {}

    payload["user"] = user_data
    payload["exp"] = datetime.now() + expiry
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        payload=payload,
        key=settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


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

