#  combination of sqlalchemy and sqlmodel for better database control
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings
from app.models.books import Book

# Create async engine
async_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,  # Optional: for logging SQL statements
    future=True
)

# Initialize database
async def init_db() -> None:
    async with async_engine.begin() as conn:
        print("Creating tables...")
        await conn.run_sync(SQLModel.metadata.create_all)
        print("Tables created")

# Session dependency
async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


# SQL model way of doing things. 
# from sqlmodel import SQLModel
# from sqlmodel.ext.asyncio.session import AsyncSession
# from sqlmodel.ext.asyncio.session import AsyncEngine as SQLModelAsyncEngine
# from sqlmodel import create_engine
# from app.core.config import settings

# # Create engine - SQLModel way
# engine = create_engine(
#     settings.DATABASE_URL,
#     echo=settings.DB_ECHO,
#     future=True
# )

# # Initialize database
# async def init_db() -> None:
#     async with SQLModelAsyncEngine(engine).begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)

# # Session dependency
# async def get_session() -> AsyncSession:
#     async with AsyncSession(engine) as session:
#         try:
#             yield session
#         finally:
#             await session.close()
