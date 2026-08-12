import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.fuel import FuelRecord
from app.models.vehicle import Vehicle
from app.schemas.fuel import FuelCreate, FuelUpdate
from app.services.fuel_service import FuelService


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_fuel.db"

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


def create_test_fuel(db):
    vehicle = create_test_vehicle(db)

    fuel_data = FuelCreate(
        vehicle_id=vehicle.id,
        fuel_type="diesel",
        quantity_liters=50,
        price_per_liter=90,
        odometer=10500,
    )

    return FuelService.create_fuel_record(
        db,
        fuel_data,
    )


def test_create_fuel_record(db):
    fuel = create_test_fuel(db)

    assert fuel.id is not None
    assert fuel.vehicle_id is not None
    assert fuel.fuel_type == "diesel"
    assert fuel.quantity_liters == 50
    assert fuel.price_per_liter == 90
    assert fuel.total_cost == 4500
    assert fuel.odometer == 10500


def test_get_fuel_records(db):
    create_test_fuel(db)

    records = FuelService.get_fuel_records(db)

    assert len(records) == 1
    assert records[0].quantity_liters == 50


def test_get_fuel_record(db):
    fuel = create_test_fuel(db)

    result = FuelService.get_fuel_record(
        db,
        fuel.id,
    )

    assert result.id == fuel.id
    assert result.total_cost == 4500


def test_get_fuel_record_not_found(db):
    with pytest.raises(
        LookupError,
        match="Fuel record not found",
    ):
        FuelService.get_fuel_record(
            db,
            99999,
        )


def test_create_fuel_vehicle_not_found(db):
    fuel_data = FuelCreate(
        vehicle_id=99999,
        fuel_type="diesel",
        quantity_liters=50,
        price_per_liter=90,
        odometer=10000,
    )

    with pytest.raises(
        LookupError,
        match="Vehicle not found",
    ):
        FuelService.create_fuel_record(
            db,
            fuel_data,
        )


def test_create_fuel_invalid_quantity(db):
    vehicle = create_test_vehicle(db)

    fuel_data = FuelCreate(
        vehicle_id=vehicle.id,
        fuel_type="diesel",
        quantity_liters=0,
        price_per_liter=90,
        odometer=10000,
    )

    with pytest.raises(
        ValueError,
        match="Fuel quantity must be greater than zero",
    ):
        FuelService.create_fuel_record(
            db,
            fuel_data,
        )


def test_create_fuel_negative_price(db):
    vehicle = create_test_vehicle(db)

    fuel_data = FuelCreate(
        vehicle_id=vehicle.id,
        fuel_type="diesel",
        quantity_liters=50,
        price_per_liter=-10,
        odometer=10000,
    )

    with pytest.raises(
        ValueError,
        match="Price per liter cannot be negative",
    ):
        FuelService.create_fuel_record(
            db,
            fuel_data,
        )


def test_vehicle_odometer_updates(db):
    vehicle = create_test_vehicle(db)

    fuel_data = FuelCreate(
        vehicle_id=vehicle.id,
        fuel_type="diesel",
        quantity_liters=40,
        price_per_liter=90,
        odometer=15000,
    )

    FuelService.create_fuel_record(
        db,
        fuel_data,
    )

    db.refresh(vehicle)

    assert vehicle.current_km == 15000


def test_update_fuel_record(db):
    fuel = create_test_fuel(db)

    update_data = FuelUpdate(
        quantity_liters=60,
        price_per_liter=95,
        odometer=16000,
    )

    updated = FuelService.update_fuel_record(
        db,
        fuel.id,
        update_data,
    )

    assert updated.quantity_liters == 60
    assert updated.price_per_liter == 95
    assert updated.odometer == 16000
    assert updated.total_cost == 5700


def test_update_fuel_type(db):
    fuel = create_test_fuel(db)

    update_data = FuelUpdate(
        fuel_type="petrol",
    )

    updated = FuelService.update_fuel_record(
        db,
        fuel.id,
        update_data,
    )

    assert updated.fuel_type == "petrol"


def test_delete_fuel_record(db):
    fuel = create_test_fuel(db)

    FuelService.delete_fuel_record(
        db,
        fuel.id,
    )

    deleted = (
        db.query(FuelRecord)
        .filter(FuelRecord.id == fuel.id)
        .first()
    )

    assert deleted is None