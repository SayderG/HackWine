from typing import Optional, List
from sqlmodel import SQLModel, Field
from sqlmodel import Relationship
from .columns import Columns

class FunnelBase(SQLModel):
    name: str


class Funnels(FunnelBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    columns: List["Columns"] = Relationship(back_populates="funnel", sa_relationship_kwargs={"lazy": 'selectin'})


class FunnelCreate(FunnelBase):
    pass


class FunnelRead(FunnelBase):
    id: int
    pass


class FunnelReadAll(FunnelRead):
    columns: List["Columns"]
    pass
