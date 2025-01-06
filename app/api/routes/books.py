from typing import List
from fastapi import APIRouter, Depends, Query
from app.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.books import BookCreate, BookPublic, BookUpdate
from app.services.books import BookService

router = APIRouter()
book_service = BookService()


@router.post("/books", response_model= BookPublic)
async def create_book(book: BookCreate, session:AsyncSession=Depends(get_session)):
    new_book =  await book_service.create_book(book, session)
    return new_book


@router.get("/books", response_model=List[BookPublic])
async def read_books(
    session: AsyncSession = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=20, le=100)
):
    # Fix the parameter order to match the service method
    books_data = await book_service.read_books(offset, limit, session)
    return books_data


@router.get("/books/{book_id}", response_model=BookPublic)
async def read_book(book_id:int, session:AsyncSession=Depends(get_session)):
    book_data = await book_service.read_book(book_id, session)
    return book_data


@router.delete("/books/{book_id}", response_model=BookPublic)
async def delete_book(book_id:int, session:AsyncSession = Depends(get_session)):
    deleted_book = await book_service.delete_book(book_id, session)
    return deleted_book


@router.put("/books/{book_id}", response_model=BookPublic)
async def update_book(book_id:int, book: BookUpdate ,session:AsyncSession=Depends(get_session)):
    updated_book = await book_service.update_book(book_id, book, session)
    return updated_book