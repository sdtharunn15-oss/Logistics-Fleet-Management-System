import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.driver import Driver
from app.schemas.driver import DriverCreate, DriverUpdate
from app.services.driver_service import DriverService


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_drivers.db"

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


def create_test_driver(db):
    driver_data = DriverCreate(
        name="Arun Kumar",
        license_number="TN-DL-12345",
        phone="9876543210",
        email="arun@example.com",
        experience_years=5,
        is_available=True,
    )

    return DriverService.create_driver(
        db,
        driver_data,
    )


def test_create_driver(db):
    driver = create_test_driver(db)

    assert driver.id is not None
    assert driver.name == "Arun Kumar"
    assert driver.license_number == "TN-DL-12345"
    assert driver.phone == "9876543210"
    assert driver.email == "arun@example.com"
    assert driver.experience_years == 5
    assert driver.is_available is True


def test_get_drivers(db):
    create_test_driver(db)

    drivers = DriverService.get_drivers(db)

    assert len(drivers) == 1
    assert drivers[0].name == "Arun Kumar"


def test_get_driver(db):
    driver = create_test_driver(db)

    result = DriverService.get_driver(
        db,
        driver.id,
    )

    assert result.id == driver.id
    assert result.license_number == "TN-DL-12345"


def test_get_driver_not_found(db):
    with pytest.raises(
        LookupError,
        match="Driver not found",
    ):
        DriverService.get_driver(
            db,
            99999,
        )


def test_duplicate_license_number(db):
    create_test_driver(db)

    driver_data = DriverCreate(
        name="Ravi Kumar",
        license_number="TN-DL-12345",
        phone="9876500000",
        email="ravi@example.com",
        experience_years=3,
    )

    with pytest.raises(
        ValueError,
        match="License number already exists",
    ):
        DriverService.create_driver(
            db,
            driver_data,
        )


def test_duplicate_email(db):
    create_test_driver(db)

    driver_data = DriverCreate(
        name="Ravi Kumar",
        license_number="TN-DL-99999",
        phone="9876500000",
        email="arun@example.com",
        experience_years=3,
    )

    with pytest.raises(
        ValueError,
        match="Email already exists",
    ):
        DriverService.create_driver(
            db,
            driver_data,
        )


def test_create_driver_without_email(db):
    driver_data = DriverCreate(
        name="Suresh Kumar",
        license_number="TN-DL-55555",
        phone="9876511111",
        experience_years=2,
    )

    driver = DriverService.create_driver(
        db,
        driver_data,
    )

    assert driver.id is not None
    assert driver.email is None


def test_update_driver(db):
    driver = create_test_driver(db)

    update_data = DriverUpdate(
        name="Arun Raj",
        phone="9999999999",
        experience_years=7,
    )

    updated = DriverService.update_driver(
        db,
        driver.id,
        update_data,
    )

    assert updated.name == "Arun Raj"
    assert updated.phone == "9999999999"
    assert updated.experience_years == 7


def test_update_driver_license(db):
    driver = create_test_driver(db)

    update_data = DriverUpdate(
        license_number="TN-DL-77777",
    )

    updated = DriverService.update_driver(
        db,
        driver.id,
        update_data,
    )

    assert updated.license_number == "TN-DL-77777"


def test_update_duplicate_license_number(db):
    create_test_driver(db)

    second_driver = Driver(
        name="Ravi Kumar",
        license_number="TN-DL-22222",
        phone="9876522222",
        email="ravi@example.com",
        experience_years=3,
        is_available=True,
    )

    db.add(second_driver)
    db.commit()
    db.refresh(second_driver)

    update_data = DriverUpdate(
        license_number="TN-DL-12345",
    )

    with pytest.raises(
        ValueError,
        match="License number already exists",
    ):
        DriverService.update_driver(
            db,
            second_driver.id,
            update_data,
        )


def test_update_duplicate_email(db):
    create_test_driver(db)

    second_driver = Driver(
        name="Ravi Kumar",
        license_number="TN-DL-22222",
        phone="9876522222",
        email="ravi@example.com",
        experience_years=3,
        is_available=True,
    )

    db.add(second_driver)
    db.commit()
    db.refresh(second_driver)

    update_data = DriverUpdate(
        email="arun@example.com",
    )

    with pytest.raises(
        ValueError,
        match="Email already exists",
    ):
        DriverService.update_driver(
            db,
            second_driver.id,
            update_data,
        )


def test_delete_driver(db):
    driver = create_test_driver(db)

    DriverService.delete_driver(
        db,
        driver.id,
    )

    deleted = (
        db.query(Driver)
        .filter(Driver.id == driver.id)
        .first()
    )

    assert deleted is None