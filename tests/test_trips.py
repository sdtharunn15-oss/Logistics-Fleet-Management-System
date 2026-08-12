import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.driver import Driver
from app.models.trip import Trip
from app.models.vehicle import Vehicle
from app.schemas.trip import TripCreate, TripUpdate
from app.services.trip_service import TripService


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_trips.db"

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


def create_test_driver(db):
    driver = Driver(
        name="Arun Kumar",
        license_number="TN-DL-12345",
        phone="9876543210",
        email="arun@example.com",
        experience_years=5,
        is_available=True,
    )

    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver


def create_test_trip(db):
    vehicle = create_test_vehicle(db)
    driver = create_test_driver(db)

    trip_data = TripCreate(
        vehicle_id=vehicle.id,
        driver_id=driver.id,
        origin="Chennai",
        destination="Bangalore",
        distance_km=350,
        status="planned",
    )

    return TripService.create_trip(
        db,
        trip_data,
    )


def test_create_trip(db):
    trip = create_test_trip(db)

    assert trip.id is not None
    assert trip.origin == "Chennai"
    assert trip.destination == "Bangalore"
    assert trip.distance_km == 350
    assert trip.status == "planned"


def test_create_trip_assigns_vehicle(db):
    trip = create_test_trip(db)

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == trip.vehicle_id)
        .first()
    )

    assert vehicle.status == "Assigned"


def test_get_trips(db):
    create_test_trip(db)

    trips = TripService.get_trips(db)

    assert len(trips) == 1
    assert trips[0].origin == "Chennai"


def test_get_trip(db):
    trip = create_test_trip(db)

    result = TripService.get_trip(
        db,
        trip.id,
    )

    assert result.id == trip.id
    assert result.destination == "Bangalore"


def test_get_trip_not_found(db):
    with pytest.raises(
        LookupError,
        match="Trip not found",
    ):
        TripService.get_trip(
            db,
            99999,
        )


def test_create_trip_vehicle_not_found(db):
    driver = create_test_driver(db)

    trip_data = TripCreate(
        vehicle_id=99999,
        driver_id=driver.id,
        origin="Chennai",
        destination="Bangalore",
        distance_km=350,
    )

    with pytest.raises(
        LookupError,
        match="Vehicle not found",
    ):
        TripService.create_trip(
            db,
            trip_data,
        )


def test_create_trip_driver_not_found(db):
    vehicle = create_test_vehicle(db)

    trip_data = TripCreate(
        vehicle_id=vehicle.id,
        driver_id=99999,
        origin="Chennai",
        destination="Bangalore",
        distance_km=350,
    )

    with pytest.raises(
        LookupError,
        match="Driver not found",
    ):
        TripService.create_trip(
            db,
            trip_data,
        )


def test_create_trip_vehicle_not_available(db):
    vehicle = create_test_vehicle(db)
    driver = create_test_driver(db)

    vehicle.status = "Assigned"
    db.commit()

    trip_data = TripCreate(
        vehicle_id=vehicle.id,
        driver_id=driver.id,
        origin="Chennai",
        destination="Bangalore",
        distance_km=350,
    )

    with pytest.raises(
        ValueError,
        match="Vehicle is not available for assignment",
    ):
        TripService.create_trip(
            db,
            trip_data,
        )


def test_update_trip(db):
    trip = create_test_trip(db)

    update_data = TripUpdate(
        origin="Chennai",
        destination="Hyderabad",
        distance_km=630,
    )

    updated = TripService.update_trip(
        db,
        trip.id,
        update_data,
    )

    assert updated.origin == "Chennai"
    assert updated.destination == "Hyderabad"
    assert updated.distance_km == 630


def test_update_trip_status_in_progress(db):
    trip = create_test_trip(db)

    update_data = TripUpdate(
        status="in_progress",
    )

    updated = TripService.update_trip(
        db,
        trip.id,
        update_data,
    )

    assert updated.status == "in_progress"


def test_invalid_trip_status(db):
    trip = create_test_trip(db)

    update_data = TripUpdate(
        status="invalid",
    )

    with pytest.raises(
        ValueError,
        match="Invalid trip status",
    ):
        TripService.update_trip(
            db,
            trip.id,
            update_data,
        )


def test_complete_trip_releases_vehicle(db):
    trip = create_test_trip(db)

    update_data = TripUpdate(
        status="completed",
    )

    updated = TripService.update_trip(
        db,
        trip.id,
        update_data,
    )

    assert updated.status == "completed"

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == trip.vehicle_id)
        .first()
    )

    assert vehicle.status == "Available"


def test_cancel_trip_releases_vehicle(db):
    trip = create_test_trip(db)

    update_data = TripUpdate(
        status="cancelled",
    )

    updated = TripService.update_trip(
        db,
        trip.id,
        update_data,
    )

    assert updated.status == "cancelled"

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == trip.vehicle_id)
        .first()
    )

    assert vehicle.status == "Available"


def test_delete_active_trip_releases_vehicle(db):
    trip = create_test_trip(db)

    TripService.delete_trip(
        db,
        trip.id,
    )

    deleted = (
        db.query(Trip)
        .filter(Trip.id == trip.id)
        .first()
    )

    assert deleted is None

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == trip.vehicle_id)
        .first()
    )

    assert vehicle.status == "Available"


def test_delete_completed_trip_does_not_change_vehicle(db):
    trip = create_test_trip(db)

    trip.status = "completed"
    db.commit()

    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == trip.vehicle_id)
        .first()
    )

    vehicle.status = "Available"
    db.commit()

    TripService.delete_trip(
        db,
        trip.id,
    )

    deleted = (
        db.query(Trip)
        .filter(Trip.id == trip.id)
        .first()
    )

    assert deleted is None
    assert vehicle.status == "Available"