from sqlmodel import SQLModel, Field
from datetime import datetime, date, timezone
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg

class BookBase(SQLModel):
    title: str = Field(min_length=1, max_length=200, index=True)
    author: str = Field(min_length=1, max_length=100, index=True)
    publiser: str = Field(max_length=100)
    published_date: date
    page_count: int = Field(gt=0)
    language: str = Field(max_length=2)


class BookCreate(BookBase):
    pass

class BookPublic(BookBase):
    id: int
    created_at: datetime  # Expose timestamps in the read model
    updated_at: datetime

class BookUpdate(SQLModel):
    title: str | None = Field(min_length=1, max_length=200, default=None)
    author: str | None = Field(min_length=1, max_length=100, default=None)
    publiser: str | None = Field(max_length=100, default=None)
    published_date: date | None = None
    page_count: int | None = Field(gt=0, default=None)
    language: str | None = Field(max_length=2, default=None)

# Table model inherits from both BookBase and TimestampMixin
class Book(BookBase, table=True):
    id: int | None = Field(default=None, primary_key=True) # this is optional because the id is created only in the database
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(  
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    )

    def __repr__(self)->str:
        return f"<Book title={self.title} author={self.author}>"

