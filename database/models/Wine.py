from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from database.models.wineStages import Wine_stages


class WineBase(SQLModel):
    title: str = Field(default="SuperWine", max_length=50)


class Wines(WineBase, table=True):
    id: Optional[int] = Field(primary_key=True)

    stages: List[Wine_stages] = Relationship(back_populates="wine", sa_relationship_kwargs={"lazy": 'selectin',
                                                                                            "order_by": "Wine_stages.id"})


class WineCreate(WineBase):
    pass


class WineRead(WineBase):
    id: int

    stages: List[Wine_stages]
