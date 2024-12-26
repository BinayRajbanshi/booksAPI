from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.main import init_db
from app.core.config import settings
from app.api.main import api_router

description = """
A REST API for a book review web service.

Tring out various features offered by FastAPI after updation of sqlalchemy and sqlmodel

This REST API is able to;
- Create Read Update And delete books
- Add reviews to books
- Add tags to Books
    """

@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server Start...") 
    await init_db()
    yield
    print("Server Stop...") 


app = FastAPI(
    title='Simple but Scalable Fast API',
    description=description,
    lifespan=life_span,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

app.include_router(api_router, prefix=settings.API_V1_STR)
