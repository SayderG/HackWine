import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import condecimal, validator
from fastapi import HTTPException


class CardBase(SQLModel):
    author: str = Field(default='Иван Иванов')
    title: str
    subtitle: str
    type: str
    description: str
    createdAt: datetime.datetime = Field(default_factory=datetime.datetime.now)
    active: bool = Field(default=True)


class Cards(CardBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    column_id: int = Field(foreign_key="columns.id")
    column: Optional["Columns"] = Relationship(back_populates="cards", sa_relationship_kwargs={"lazy": 'selectin'})


class CardCreate(CardBase):
    column_id: int

    @validator('column_id')
    def validate_column_id(cls, value):
        if value >= 1:
            return value
        else:
            raise HTTPException(404, detail='column_id most be >= 1')


class CardRead(CardBase):
    id: int
    column_id: int
