import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class WineStageBase(SQLModel):
    name: str = Field(default="SuperWine", max_length=50)
    status: str = Field(default="new")
    location: str = Field(default="cell")


class Wine_stages(WineStageBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    wine_id: Optional[int] = Field(default=None, foreign_key="wines.id")
    started_at: datetime.datetime = Field(default=None, nullable=True)
    changed_at: datetime.datetime = Field(default=None, nullable=True)
    last: bool = Field(default=False)

    wine: Optional["Wines"] = Relationship(back_populates="stages", sa_relationship_kwargs={"lazy": 'selectin'})


class WineStageCreate(WineStageBase):
    pass


class WineStageRead(WineStageBase):
    id: int
