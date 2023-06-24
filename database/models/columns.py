from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from database.models.cards import Cards

class ColumnBase(SQLModel):
    title: str
    count: Optional[int] = Field(default=0, nullable=True)


class Columns(ColumnBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    cards: List[Cards] = Relationship(back_populates="column", sa_relationship_kwargs={"lazy": 'selectin'})


class ColumnCreate(ColumnBase):
    pass


class ColumnRead(ColumnBase):
    id: int
    pass


class ColumnReadWithCards(ColumnRead):
    cards: List[Cards]
