import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import condecimal


class SelBase(SQLModel):
    lat: condecimal(max_digits=18, decimal_places=15)
    lon: condecimal(max_digits=18, decimal_places=15)
    name: str
    desc: str


class Sellen(SelBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class SelCreate(SelBase):
    pass


class SelRead(SelBase):
    id: int
