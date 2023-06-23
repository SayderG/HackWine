from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class ColumnBase(SQLModel):
    title: str
    count: Optional[int] = Field(default=0, nullable=True)


class Columns(ColumnBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    funnel_id: int = Field(foreign_key="funnels.id")
    funnel: Optional["Funnels"] = Relationship(back_populates="columns", sa_relationship_kwargs={"lazy": 'selectin'})
    cards: List["Cards"] = Relationship(back_populates="column", sa_relationship_kwargs={"lazy": 'selectin'})


class ColumnCreate(ColumnBase):
    pass


class ColumnRead(ColumnBase):
    id: int
    pass


class ColumnReadWithCount(ColumnBase):
    id: int
    pass
