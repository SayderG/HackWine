from typing import Optional, List
from sqlmodel import SQLModel, Field, DECIMAL


class CellPredictBase(SQLModel):
    place: int = Field(foreign_key="cells.id", description="Cell id foreign key")
    latitude: float
    longitude: float
    humidity_1: Optional[int] = Field(default=0)
    humidity_2: Optional[int] = Field(default=0)
    humidity_3: Optional[int] = Field(default=0)
    humidity_4: Optional[int] = Field(default=0)
    humidity_5: Optional[int] = Field(default=0)
    temperature_1: Optional[int] = Field(default=0)
    temperature_2: Optional[int] = Field(default=0)
    temperature_3: Optional[int] = Field(default=0)
    temperature_4: Optional[int] = Field(default=0)
    temperature_5: Optional[int] = Field(default=0)
    fenophase: Optional[str] = Field(default=0)
    sugar_percent: Optional[int] = Field(default=0)
    acid_percent: Optional[int] = Field(default=0)
    fenols_percent: Optional[int] = Field(default=0)
    alkans_percent: Optional[int] = Field(default=0)
    evi: Optional[float] = Field(default=0)
    previous_stage_success: float = Field(default=0)
    temperature_forecast_1: Optional[int] = Field(default=0)
    temperature_forecast_2: Optional[int] = Field(default=0)
    temperature_forecast_3: Optional[int] = Field(default=0)
    temperature_forecast_4: Optional[int] = Field(default=0)
    temperature_forecast_5: Optional[int] = Field(default=0)
    rain_1: Optional[bool] = Field(default=False)
    rain_2: Optional[bool] = Field(default=False)
    rain_3: Optional[bool] = Field(default=False)
    rain_4: Optional[bool] = Field(default=False)
    rain_5: Optional[bool] = Field(default=False)
    density: int = Field(default=0)


class Cell_predicts(CellPredictBase, table=True):
    id: Optional[int] = Field(primary_key=True)


class CellPredictCreate(CellPredictBase):
    pass


class CellPredictRead(CellPredictBase):
    id: int
