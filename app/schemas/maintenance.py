from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MaintenanceBase(BaseModel):
    vehicle_id: int
    maintenance_type: str
    description: Optional[str] = None
    cost: float = 0
    status: str = "scheduled"


class MaintenanceCreate(MaintenanceBase):
    maintenance_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None


class MaintenanceUpdate(BaseModel):
    maintenance_type: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[float] = None
    status: Optional[str] = None
    completed_date: Optional[datetime] = None


class MaintenanceResponse(MaintenanceBase):
    id: int
    maintenance_date: datetime
    completed_date: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)