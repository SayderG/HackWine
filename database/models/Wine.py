import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class WineBase(SQLModel):
    name: str = Field(default="SuperWine", max_length=50)
    status: str = Field(default="new")
    location: str = Field(default="cell")


class Wines(WineBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


class WineCreate(WineBase):
    pass


class WineUpdate(WineBase):
    updated_at: datetime.datetime


class WineRead(WineBase):
    id: int
