from fastapi import APIRouter
from app.api.routes import books

api_router = APIRouter()
api_router.include_router(books.router, tags=["Books"]) 


#Related endpoints are grouped together logically, Users can filter/search endpoints by their tags in the documentation interface