from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects import postgresql as pg

class TimestampModel(SQLModel):
    created_at: datetime = Field(
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    )
    updated_at: datetime = Field(  
        sa_column=Column(pg.TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    )