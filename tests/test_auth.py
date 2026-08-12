import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.schemas.auth import UserLogin, UserRegister
from app.services.auth_service import AuthService
from app.utils.security import decode_access_token


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"

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


def create_test_user(db):
    user_data = UserRegister(
        name="Admin User",
        email="admin@example.com",
        password="Admin@123",
        role="Admin",
    )

    return AuthService.register_user(
        db,
        user_data,
    )


def test_register_user(db):
    user = create_test_user(db)

    assert user.id is not None
    assert user.name == "Admin User"
    assert user.email == "admin@example.com"
    assert user.role == "Admin"
    assert user.is_active is True

    # Password should never be stored as plain text.
    assert user.hashed_password != "Admin@123"


def test_register_driver(db):
    user_data = UserRegister(
        name="Driver User",
        email="driver@example.com",
        password="Driver@123",
        role="Driver",
    )

    user = AuthService.register_user(
        db,
        user_data,
    )

    assert user.role == "Driver"


def test_register_fleet_manager(db):
    user_data = UserRegister(
        name="Fleet Manager",
        email="manager@example.com",
        password="Manager@123",
        role="Fleet Manager",
    )

    user = AuthService.register_user(
        db,
        user_data,
    )

    assert user.role == "Fleet Manager"


def test_invalid_role(db):
    user_data = UserRegister(
        name="Test User",
        email="test@example.com",
        password="Test@123",
        role="Customer",
    )

    with pytest.raises(
        ValueError,
        match="Invalid role",
    ):
        AuthService.register_user(
            db,
            user_data,
        )


def test_duplicate_email(db):
    create_test_user(db)

    user_data = UserRegister(
        name="Another User",
        email="admin@example.com",
        password="Another@123",
        role="Driver",
    )

    with pytest.raises(
        ValueError,
        match="Email already registered",
    ):
        AuthService.register_user(
            db,
            user_data,
        )


def test_authenticate_user(db):
    create_test_user(db)

    login_data = UserLogin(
        email="admin@example.com",
        password="Admin@123",
    )

    user = AuthService.authenticate_user(
        db,
        login_data,
    )

    assert user.id is not None
    assert user.email == "admin@example.com"
    assert user.role == "Admin"


def test_invalid_password(db):
    create_test_user(db)

    login_data = UserLogin(
        email="admin@example.com",
        password="WrongPassword@123",
    )

    with pytest.raises(
        ValueError,
        match="Invalid email or password",
    ):
        AuthService.authenticate_user(
            db,
            login_data,
        )


def test_invalid_email(db):
    login_data = UserLogin(
        email="missing@example.com",
        password="Admin@123",
    )

    with pytest.raises(
        ValueError,
        match="Invalid email or password",
    ):
        AuthService.authenticate_user(
            db,
            login_data,
        )


def test_inactive_user(db):
    user = create_test_user(db)

    user.is_active = False
    db.commit()

    login_data = UserLogin(
        email="admin@example.com",
        password="Admin@123",
    )

    with pytest.raises(
        PermissionError,
        match="User account is inactive",
    ):
        AuthService.authenticate_user(
            db,
            login_data,
        )


def test_create_access_token(db):
    user = create_test_user(db)

    token = AuthService.create_token(user)

    assert token is not None
    assert isinstance(token, str)
    assert len(token) > 0


def test_access_token_payload(db):
    user = create_test_user(db)

    token = AuthService.create_token(user)

    payload = decode_access_token(token)

    assert payload["sub"] == str(user.id)
    assert payload["role"] == "Admin"
    assert "exp" in payload