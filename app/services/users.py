from fastapi import HTTPException, status
from app.models.users import User,UserCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import select, desc

class UserService:
    async def read_user_by_email(self, email:EmailStr, session:AsyncSession):
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first()
    

    async def read_user_by_username(self, username:str, session:AsyncSession):
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first()
    

    async def email_exists(self, email:EmailStr, session:AsyncSession)->bool:
        email_exists = await self.read_user_by_email(email, session)
        return True if email_exists is not None else False

    async def username_exists(self,  username:str, session:AsyncSession)->bool:
        username_exists = await self.read_user_by_username(username, session)
        return True if  username_exists is not None else False

    async def create_user(self, user_data:UserCreate, session:AsyncSession):
        user_dict = user_data.model_dump()

        print("incoming data", user_dict)

        username_exists = await self.username_exists(user_dict["username"], session)
        if username_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Username is already taken")

        email_exists = await self.email_exists(user_dict["email"], session)
        if email_exists:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email is already taken")
            
        user_dict["created_at"] = datetime.now()
        user_dict["updated_at"] = datetime.now()
        user_dict["hashed_password"] = "helloworld"
        db_user = User.model_validate(user_dict)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user
    
    
    async def read_users(self, limit:int,offset:int, session:AsyncSession):
        statement = select(User).limit(limit).offset(offset).order_by(desc(User.created_at))
        result = await session.exec(statement)
        return result.all()
    

    async def read_user(self, id:int, session:AsyncSession):
        result = await session.get(User, id)
        if not result:
            raise HTTPException(status_code=404, detail="User not found")
        return result
