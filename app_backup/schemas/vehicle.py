from pydantic import BaseModel, ConfigDict, Field


class VehicleBase(BaseModel):
    vehicle_number: str = Field(
        min_length=2,
        max_length=50,
    )

    vehicle_type: str = Field(
        min_length=2,
        max_length=50,
    )

    model: str = Field(
        min_length=1,
        max_length=100,
    )

    manufacturing_year: int = Field(
        ge=1900,
        le=2100,
    )

    capacity: float = Field(
        gt=0,
    )

    current_km: float = Field(
        ge=0,
    )


class VehicleCreate(VehicleBase):
    pass


class VehicleUpdate(BaseModel):
    vehicle_number: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    vehicle_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )

    model: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )

    manufacturing_year: int | None = Field(
        default=None,
        ge=1900,
        le=2100,
    )

    capacity: float | None = Field(
        default=None,
        gt=0,
    )

    current_km: float | None = Field(
        default=None,
        ge=0,
    )

    status: str | None = None


class VehicleResponse(VehicleBase):
    id: int
    status: str

    model_config = ConfigDict(
        from_attributes=True,
    )