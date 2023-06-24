import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import condecimal


class PointBase(SQLModel):
    lat: condecimal(max_digits=18, decimal_places=15)
    lon: condecimal(max_digits=18, decimal_places=15)
    name: str
    desc: str
    severity: str


class Points(PointBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    created_ad: datetime.datetime = Field(default_factory=datetime.datetime.now)


class PointCreate(PointBase):
    pass


class PointRead(PointBase):
    id: int
    created_ad: datetime.datetime