from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class FuelBase(BaseModel):
    vehicle_id: int
    fuel_type: str = "diesel"
    quantity_liters: float
    price_per_liter: float
    odometer: float = 0


class FuelCreate(FuelBase):
    fuel_date: Optional[datetime] = None


class FuelUpdate(BaseModel):
    fuel_type: Optional[str] = None
    quantity_liters: Optional[float] = None
    price_per_liter: Optional[float] = None
    odometer: Optional[float] = None


class FuelResponse(FuelBase):
    id: int
    total_cost: float
    fuel_date: datetime

    model_config = ConfigDict(from_attributes=True)