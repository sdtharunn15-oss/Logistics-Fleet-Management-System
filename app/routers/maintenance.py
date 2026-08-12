from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.maintenance import MaintenanceRecord
from app.models.vehicle import Vehicle
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceResponse,
    MaintenanceUpdate,
)


router = APIRouter(
    prefix="/maintenance",
    tags=["Maintenance"],
)


@router.get("", response_model=list[MaintenanceResponse])
def get_maintenance_records(db: Session = Depends(get_db)):
    return db.query(MaintenanceRecord).all()


@router.post(
    "",
    response_model=MaintenanceResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_maintenance(
    maintenance_data: MaintenanceCreate,
    db: Session = Depends(get_db),
):
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == maintenance_data.vehicle_id)
        .first()
    )

    if not vehicle:
        raise HTTPException(
            status_code=404,
            detail="Vehicle not found",
        )

    data = maintenance_data.model_dump()

    if data.get("maintenance_date") is None:
        data.pop("maintenance_date", None)

    maintenance = MaintenanceRecord(**data)

    db.add(maintenance)
    db.commit()
    db.refresh(maintenance)

    return maintenance


@router.get("/{maintenance_id}", response_model=MaintenanceResponse)
def get_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    maintenance = (
        db.query(MaintenanceRecord)
        .filter(MaintenanceRecord.id == maintenance_id)
        .first()
    )

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    return maintenance


@router.put(
    "/{maintenance_id}",
    response_model=MaintenanceResponse,
)
def update_maintenance(
    maintenance_id: int,
    maintenance_data: MaintenanceUpdate,
    db: Session = Depends(get_db),
):
    maintenance = (
        db.query(MaintenanceRecord)
        .filter(MaintenanceRecord.id == maintenance_id)
        .first()
    )

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    update_data = maintenance_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(maintenance, field, value)

    db.commit()
    db.refresh(maintenance)

    return maintenance


@router.delete("/{maintenance_id}")
def delete_maintenance(
    maintenance_id: int,
    db: Session = Depends(get_db),
):
    maintenance = (
        db.query(MaintenanceRecord)
        .filter(MaintenanceRecord.id == maintenance_id)
        .first()
    )

    if not maintenance:
        raise HTTPException(
            status_code=404,
            detail="Maintenance record not found",
        )

    db.delete(maintenance)
    db.commit()

    return {
        "message": "Maintenance record deleted successfully"
    }