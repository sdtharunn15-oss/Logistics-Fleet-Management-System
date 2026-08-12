from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vehicle import Vehicle
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.fuel import FuelRecord
from app.models.maintenance import MaintenanceRecord


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total_vehicles = db.query(func.count(Vehicle.id)).scalar() or 0
    total_drivers = db.query(func.count(Driver.id)).scalar() or 0
    total_trips = db.query(func.count(Trip.id)).scalar() or 0
    total_fuel_records = db.query(func.count(FuelRecord.id)).scalar() or 0
    total_maintenance = (
        db.query(func.count(MaintenanceRecord.id)).scalar() or 0
    )

    total_fuel_cost = (
        db.query(func.sum(FuelRecord.total_cost)).scalar() or 0
    )

    total_maintenance_cost = (
        db.query(func.sum(MaintenanceRecord.cost)).scalar() or 0
    )

    return {
        "total_vehicles": total_vehicles,
        "total_drivers": total_drivers,
        "total_trips": total_trips,
        "total_fuel_records": total_fuel_records,
        "total_maintenance_records": total_maintenance,
        "total_fuel_cost": float(total_fuel_cost),
        "total_maintenance_cost": float(total_maintenance_cost),
    }