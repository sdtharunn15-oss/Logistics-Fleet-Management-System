from typing import Optional

from pydantic import BaseModel, ConfigDict


class DriverBase(BaseModel):
    name: str
    license_number: str
    phone: str
    email: Optional[str] = None
    experience_years: int = 0
    is_available: bool = True


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    license_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    experience_years: Optional[int] = None
    is_available: Optional[bool] = None


class DriverResponse(DriverBase):
    id: int

    model_config = ConfigDict(from_attributes=True)