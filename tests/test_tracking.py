import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.tracking import TrackingRecord
from app.models.vehicle import Vehicle
from app.schemas.tracking import TrackingCreate
from app.services.tracking_service import TrackingService


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_tracking.db"

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


def create_test_tracking(db):
    vehicle = create_test_vehicle(db)

    tracking_data = TrackingCreate(
        vehicle_id=vehicle.id,
        latitude=13.0827,
        longitude=80.2707,
        speed=45,
    )

    return TrackingService.create_tracking_record(
        db,
        tracking_data,
    )


def test_create_tracking_record(db):
    record = create_test_tracking(db)

    assert record.id is not None
    assert record.vehicle_id is not None
    assert record.latitude == 13.0827
    assert record.longitude == 80.2707
    assert record.speed == 45


def test_get_tracking_records(db):
    create_test_tracking(db)

    records = TrackingService.get_tracking_records(db)

    assert len(records) == 1
    assert records[0].speed == 45


def test_get_tracking_record(db):
    record = create_test_tracking(db)

    result = TrackingService.get_tracking_record(
        db,
        record.id,
    )

    assert result.id == record.id
    assert result.vehicle_id == record.vehicle_id


def test_get_tracking_record_not_found(db):
    with pytest.raises(
        LookupError,
        match="Tracking record not found",
    ):
        TrackingService.get_tracking_record(
            db,
            99999,
        )


def test_create_tracking_vehicle_not_found(db):
    tracking_data = TrackingCreate(
        vehicle_id=99999,
        latitude=13.0827,
        longitude=80.2707,
        speed=40,
    )

    with pytest.raises(
        LookupError,
        match="Vehicle not found",
    ):
        TrackingService.create_tracking_record(
            db,
            tracking_data,
        )


def test_tracking_default_speed(db):
    vehicle = create_test_vehicle(db)

    tracking_data = TrackingCreate(
        vehicle_id=vehicle.id,
        latitude=13.0827,
        longitude=80.2707,
    )

    record = TrackingService.create_tracking_record(
        db,
        tracking_data,
    )

    assert record.speed == 0


def test_delete_tracking_record(db):
    record = create_test_tracking(db)

    TrackingService.delete_tracking_record(
        db,
        record.id,
    )

    deleted = (
        db.query(TrackingRecord)
        .filter(
            TrackingRecord.id == record.id
        )
        .first()
    )

    assert deleted is None


def test_delete_tracking_record_not_found(db):
    with pytest.raises(
        LookupError,
        match="Tracking record not found",
    ):
        TrackingService.delete_tracking_record(
            db,
            99999,
        )