import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleUpdate
from app.services.vehicle_service import VehicleService


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_vehicles.db"

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
    vehicle_data = VehicleCreate(
        vehicle_number="TN01AB1234",
        vehicle_type="Truck",
        model="Tata 407",
        manufacturing_year=2022,
        capacity=5000,
        current_km=10000,
    )

    return VehicleService.create_vehicle(
        db,
        vehicle_data,
    )


def test_create_vehicle(db):
    vehicle = create_test_vehicle(db)

    assert vehicle.id is not None
    assert vehicle.vehicle_number == "TN01AB1234"
    assert vehicle.vehicle_type == "Truck"
    assert vehicle.model == "Tata 407"
    assert vehicle.status == "Available"


def test_get_vehicles(db):
    create_test_vehicle(db)

    vehicles = VehicleService.get_vehicles(db)

    assert len(vehicles) == 1
    assert vehicles[0].vehicle_number == "TN01AB1234"


def test_get_vehicle(db):
    vehicle = create_test_vehicle(db)

    result = VehicleService.get_vehicle(
        db,
        vehicle.id,
    )

    assert result.id == vehicle.id
    assert result.vehicle_number == "TN01AB1234"


def test_get_vehicle_not_found(db):
    with pytest.raises(LookupError, match="Vehicle not found"):
        VehicleService.get_vehicle(
            db,
            99999,
        )


def test_duplicate_vehicle_number(db):
    create_test_vehicle(db)

    vehicle_data = VehicleCreate(
        vehicle_number="TN01AB1234",
        vehicle_type="Truck",
        model="Ashok Leyland",
        manufacturing_year=2023,
        capacity=6000,
        current_km=5000,
    )

    with pytest.raises(
        ValueError,
        match="Vehicle number already exists",
    ):
        VehicleService.create_vehicle(
            db,
            vehicle_data,
        )


def test_update_vehicle(db):
    vehicle = create_test_vehicle(db)

    update_data = VehicleUpdate(
        model="Tata 709",
        current_km=15000,
    )

    updated = VehicleService.update_vehicle(
        db,
        vehicle.id,
        update_data,
    )

    assert updated.model == "Tata 709"
    assert updated.current_km == 15000


def test_update_vehicle_status(db):
    vehicle = create_test_vehicle(db)

    update_data = VehicleUpdate(
        status="Maintenance",
    )

    updated = VehicleService.update_vehicle(
        db,
        vehicle.id,
        update_data,
    )

    assert updated.status == "Maintenance"


def test_invalid_vehicle_status(db):
    vehicle = create_test_vehicle(db)

    update_data = VehicleUpdate(
        status="InvalidStatus",
    )

    with pytest.raises(
        ValueError,
        match="Invalid vehicle status",
    ):
        VehicleService.update_vehicle(
            db,
            vehicle.id,
            update_data,
        )


def test_update_duplicate_vehicle_number(db):
    create_test_vehicle(db)

    second_vehicle = Vehicle(
        vehicle_number="TN02CD5678",
        vehicle_type="Van",
        model="Mahindra Bolero",
        manufacturing_year=2023,
        capacity=2000,
        current_km=5000,
        status="Available",
    )

    db.add(second_vehicle)
    db.commit()
    db.refresh(second_vehicle)

    update_data = VehicleUpdate(
        vehicle_number="TN01AB1234",
    )

    with pytest.raises(
        ValueError,
        match="Vehicle number already exists",
    ):
        VehicleService.update_vehicle(
            db,
            second_vehicle.id,
            update_data,
        )


def test_delete_vehicle(db):
    vehicle = create_test_vehicle(db)

    VehicleService.delete_vehicle(
        db,
        vehicle.id,
    )

    deleted = (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle.id)
        .first()
    )

    assert deleted is None


def test_delete_assigned_vehicle(db):
    vehicle = create_test_vehicle(db)

    vehicle.status = "Assigned"
    db.commit()

    with pytest.raises(
        ValueError,
        match="Assigned vehicle cannot be deleted",
    ):
        VehicleService.delete_vehicle(
            db,
            vehicle.id,
        )