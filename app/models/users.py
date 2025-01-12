from sqlmodel import SQLModel, Field
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg
from .validators import validate_username, validate_password, validate_phone
from pydantic import EmailStr, field_validator
import uuid

class UserBase(SQLModel):
    first_name: str = Field(min_length=1, max_length=50, index=True)
    last_name: str = Field(min_length=1, max_length=50, index=True)
    email:EmailStr = Field( index = True, unique=True)
    username:str = Field(min_length=1, max_length=50, unique=True)
    phone_no: str | None = Field(min_length=10, max_length=15)
    is_verified: bool = Field(default=False)
    

    @field_validator("username")
    @classmethod
    def username_validator(cls, v):
        return validate_username(v)

    @field_validator("phone_no")
    @classmethod
    def phone_validator(cls, value):
        return validate_phone(value)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)


class UserUpdate(SQLModel):
    first_name: str | None = Field(min_length=1, max_length=50, index=True, default=None)
    last_name: str | None = Field(min_length=1, max_length=50, index=True, default=None)
    email:EmailStr | None = Field( index = True, unique=True, default=None)
    username:str | None = Field(min_length=1, max_length=50, unique=True, default=None)
    phone_no: str | None = Field(min_length=10, max_length=15, default=None)
    is_verified: bool | None = Field(default=None)
    password: str | None =  Field(min_length=8, max_length=50)

    @field_validator("username")
    @classmethod
    def username_validator(cls, v):
        return validate_username(v)

    @field_validator("phone_no")
    @classmethod
    def phone_validator(cls, value):
        return validate_phone(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        return validate_password(value)


class UserPublic(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class User(UserBase, table=True):
    id: int | None = Field(primary_key=True, default=None)
    hashed_password: str = Field()
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(  
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    )

    def __repr__(self)->str:
        return f"<User email={self.email} username={self.username}>"
    

# MODELS RELATED WITH TOKENS

# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    access_token_expires:datetime
    refresh_token: str
    refresh_token_expires:datetime
    token_type: str = "bearer"

# Contents of JWT, so that we can validate the token
class TokenData(SQLModel):
    id: int
    email: EmailStr
    username:str
    jti: str
    exp: int #UNIX timestamp
    refresh: bool
