from typing import Optional, List
from sqlmodel import SQLModel, Field, DECIMAL
from sqlalchemy import Column, ARRAY, DECIMAL, String
from decimal import Decimal


class CellBase(SQLModel):
    point1: List[Decimal] = Field(sa_column=Column(ARRAY(DECIMAL)))
    point2: List[Decimal] = Field(sa_column=Column(ARRAY(DECIMAL)))
    point3: List[Decimal] = Field(sa_column=Column(ARRAY(DECIMAL)))
    point4: List[Decimal] = Field(sa_column=Column(ARRAY(DECIMAL)))
    name: str
    desc: str
    urls: list[str] = Field(sa_column=Column(ARRAY(String)))


class Cells(CellBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class CellCreate(CellBase):
    pass


class CellRead(CellBase):
    id: int
