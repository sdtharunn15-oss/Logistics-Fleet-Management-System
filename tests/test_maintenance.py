import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.maintenance import MaintenanceRecord
from app.models.vehicle import Vehicle
from app.schemas.maintenance import (
    MaintenanceCreate,
    MaintenanceUpdate,
)
from app.services.maintenance_service import (
    MaintenanceService,
)


SQLALCHEMY_DATABASE_URL = (
    "sqlite:///./test_maintenance.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def create_test_vehicle(db):
    vehicle = Vehicle(
        vehicle_number="TN01AB1234",
        vehicle_type="Truck",
        model="Tata 407",
        manufacturing_year=2022,
        capacity=5000,
        current_km=10000,
        status="Available",
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


def create_test_maintenance(db):
    vehicle = create_test_vehicle(db)

    maintenance_data = MaintenanceCreate(
        vehicle_id=vehicle.id,
        maintenance_type="Oil Change",
        description="Engine oil replacement",
        cost=2500,
        status="scheduled",
    )

    return MaintenanceService.create_maintenance(
        db,
        maintenance_data,
    )


def test_create_maintenance(db):
    maintenance = create_test_maintenance(db)

    assert maintenance.id is not None
    assert maintenance.vehicle_id is not None
    assert maintenance.maintenance_type == "Oil Change"
    assert maintenance.description == (
        "Engine oil replacement"
    )
    assert maintenance.cost == 2500
    assert maintenance.status == "scheduled"


def test_vehicle_status_changes_to_maintenance(db):
    maintenance = create_test_maintenance(db)

    vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.id == maintenance.vehicle_id
        )
        .first()
    )

    assert vehicle.status == "Maintenance"


def test_get_maintenance_records(db):
    create_test_maintenance(db)

    records = (
        MaintenanceService.get_maintenance_records(
            db
        )
    )

    assert len(records) == 1
    assert records[0].maintenance_type == "Oil Change"


def test_get_maintenance(db):
    maintenance = create_test_maintenance(db)

    result = MaintenanceService.get_maintenance(
        db,
        maintenance.id,
    )

    assert result.id == maintenance.id
    assert result.cost == 2500


def test_get_maintenance_not_found(db):
    with pytest.raises(
        LookupError,
        match="Maintenance record not found",
    ):
        MaintenanceService.get_maintenance(
            db,
            99999,
        )


def test_create_maintenance_vehicle_not_found(db):
    maintenance_data = MaintenanceCreate(
        vehicle_id=99999,
        maintenance_type="Oil Change",
        description="Engine oil replacement",
        cost=2500,
        status="scheduled",
    )

    with pytest.raises(
        LookupError,
        match="Vehicle not found",
    ):
        MaintenanceService.create_maintenance(
            db,
            maintenance_data,
        )


def test_negative_maintenance_cost(db):
    vehicle = create_test_vehicle(db)

    maintenance_data = MaintenanceCreate(
        vehicle_id=vehicle.id,
        maintenance_type="Repair",
        description="Brake repair",
        cost=-100,
        status="scheduled",
    )

    with pytest.raises(
        ValueError,
        match="Maintenance cost cannot be negative",
    ):
        MaintenanceService.create_maintenance(
            db,
            maintenance_data,
        )


def test_invalid_maintenance_status(db):
    vehicle = create_test_vehicle(db)

    maintenance_data = MaintenanceCreate(
        vehicle_id=vehicle.id,
        maintenance_type="Repair",
        description="Brake repair",
        cost=1000,
        status="invalid",
    )

    with pytest.raises(
        ValueError,
        match="Invalid maintenance status",
    ):
        MaintenanceService.create_maintenance(
            db,
            maintenance_data,
        )


def test_update_maintenance(db):
    maintenance = create_test_maintenance(db)

    update_data = MaintenanceUpdate(
        description="Full engine service",
        cost=5000,
    )

    updated = MaintenanceService.update_maintenance(
        db,
        maintenance.id,
        update_data,
    )

    assert updated.description == (
        "Full engine service"
    )
    assert updated.cost == 5000


def test_complete_maintenance(db):
    maintenance = create_test_maintenance(db)

    update_data = MaintenanceUpdate(
        status="completed",
    )

    updated = MaintenanceService.update_maintenance(
        db,
        maintenance.id,
        update_data,
    )

    assert updated.status == "completed"

    vehicle = (
        db.query(Vehicle)
        .filter(
            Vehicle.id == maintenance.vehicle_id
        )
        .first()
    )

    assert vehicle.status == "Available"


def test_update_invalid_status(db):
    maintenance = create_test_maintenance(db)

    update_data = MaintenanceUpdate(
        status="invalid",
    )

    with pytest.raises(
        ValueError,
        match="Invalid maintenance status",
    ):
        MaintenanceService.update_maintenance(
            db,
            maintenance.id,
            update_data,
        )


def test_update_negative_cost(db):
    maintenance = create_test_maintenance(db)

    update_data = MaintenanceUpdate(
        cost=-500,
    )

    with pytest.raises(
        ValueError,
        match="Maintenance cost cannot be negative",
    ):
        MaintenanceService.update_maintenance(
            db,
            maintenance.id,
            update_data,
        )


def test_delete_maintenance(db):
    maintenance = create_test_maintenance(db)

    MaintenanceService.delete_maintenance(
        db,
        maintenance.id,
    )

    deleted = (
        db.query(MaintenanceRecord)
        .filter(
            MaintenanceRecord.id
            == maintenance.id
        )
        .first()
    )

    assert deleted is None