from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.fuel import FuelRecord
from app.models.vehicle import Vehicle
from app.schemas.fuel import FuelCreate, FuelResponse, FuelUpdate


router = APIRouter(
    prefix="/fuel",
    tags=["Fuel"],
)


@router.get("", response_model=list[FuelResponse])
def get_fuel_records(db: Session = Depends(get_db)):
    return db.query(FuelRecord).all()


@router.post(
    "",
    response_model=FuelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_fuel_record(
    fuel_data: FuelCreate,
    db: Session = Depends(get_db),
):
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == fuel_data.vehicle_id)
        .first()
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    total_cost = (
        fuel_data.quantity_liters *
        fuel_data.price_per_liter
    )

    data = fuel_data.model_dump()

    if data.get("fuel_date") is None:
        data.pop("fuel_date", None)

    fuel = FuelRecord(
        **data,
        total_cost=total_cost,
    )

    db.add(fuel)
    db.commit()
    db.refresh(fuel)

    return fuel


@router.get("/{fuel_id}", response_model=FuelResponse)
def get_fuel_record(
    fuel_id: int,
    db: Session = Depends(get_db),
):
    fuel = (
        db.query(FuelRecord)
        .filter(FuelRecord.id == fuel_id)
        .first()
    )

    if not fuel:
        raise HTTPException(
            status_code=404,
            detail="Fuel record not found",
        )

    return fuel


@router.put("/{fuel_id}", response_model=FuelResponse)
def update_fuel_record(
    fuel_id: int,
    fuel_data: FuelUpdate,
    db: Session = Depends(get_db),
):
    fuel = (
        db.query(FuelRecord)
        .filter(FuelRecord.id == fuel_id)
        .first()
    )

    if not fuel:
        raise HTTPException(
            status_code=404,
            detail="Fuel record not found",
        )

    update_data = fuel_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(fuel, field, value)

    fuel.total_cost = (
        fuel.quantity_liters *
        fuel.price_per_liter
    )

    db.commit()
    db.refresh(fuel)

    return fuel


@router.delete("/{fuel_id}")
def delete_fuel_record(
    fuel_id: int,
    db: Session = Depends(get_db),
):
    fuel = (
        db.query(FuelRecord)
        .filter(FuelRecord.id == fuel_id)
        .first()
    )

    if not fuel:
        raise HTTPException(
            status_code=404,
            detail="Fuel record not found",
        )

    db.delete(fuel)
    db.commit()

    return {
        "message": "Fuel record deleted successfully"
    }