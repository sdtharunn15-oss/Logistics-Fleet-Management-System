from fastapi import FastAPI

from app.database import Base, engine

# Import models so SQLAlchemy registers their tables
from app.models.user import User
from app.models.vehicle import Vehicle
from app.models.driver import Driver

# Import routers
from app.routers.auth import router as auth_router
from app.routers.vehicles import router as vehicle_router
from app.routers.drivers import router as driver_router
from app.models.trip import Trip
from app.routers.trips import router as trip_router
from app.models.fuel import FuelRecord
from app.routers.fuel import router as fuel_router
from app.models.maintenance import MaintenanceRecord
from app.routers.maintenance import router as maintenance_router
from app.models.tracking import TrackingRecord
from app.routers.tracking import router as tracking_router
from app.routers.dashboard import router as dashboard_router
# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Logistics & Fleet Management System",
    description="Logistics and Fleet Management REST API",
    version="1.0.0",
)


# API routers
app.include_router(auth_router)
app.include_router(vehicle_router)
app.include_router(driver_router)
app.include_router(trip_router)
app.include_router(fuel_router)
app.include_router(maintenance_router)
app.include_router(tracking_router)
app.include_router(dashboard_router)
@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Logistics & Fleet Management System API",
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
    }