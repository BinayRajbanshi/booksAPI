from app.models.books import Book, BookPublic, BookUpdate, BookCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from fastapi import Query, HTTPException
from sqlmodel import select, desc

class BookService:
    async def create_book(self, book_data:BookCreate, session:AsyncSession):
        book_dict = book_data.model_dump()
        book_dict["created_at"] = datetime.now()
        book_dict["updated_at"] = datetime.now()
        book_dict["published_date"] = datetime.strftime(book_dict["published_date"], "%Y-%m-%d" )
        db_book = Book.model_validate(book_dict)    
        session.add(db_book)
        await session.commit()
        await session.refresh(db_book)
        return db_book
    

    async def read_all_books(self, offset: int, limit: int , session: AsyncSession):
        statement = select(Book).offset(offset).limit(limit).order_by(desc(Book.created_at))
        result = await session.exec(statement)
        return result.all()
    
    
    async def read_a_book(self, id:int, session:AsyncSession):
        result = await session.get(Book, id)
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")
        return result


    async def delete_book(self, id:int, session:AsyncSession):
        result = await session.get(Book, id)
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")
        await session.delete(result)
        await session.commit()
        return result


    async def update_book(self, id:int,book: BookUpdate, session:AsyncSession):
        result = await session.get(Book, id)
        if not result:
            raise HTTPException(status_code=404, detail="Book not found")
        incoming_data = book.model_dump(exclude_unset=True)
        for key, value in incoming_data.items():
            setattr(result, key, value)
        session.add(result)
        await session.commit()
        await session.refresh(result)
        return result