from sqlalchemy import Column, Float, Integer, String

from app.database import Base


class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    vehicle_number = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    vehicle_type = Column(
        String(50),
        nullable=False,
    )

    model = Column(
        String(100),
        nullable=False,
    )

    manufacturing_year = Column(
        Integer,
        nullable=False,
    )

    capacity = Column(
        Float,
        nullable=False,
    )

    current_km = Column(
        Float,
        nullable=False,
        default=0,
    )

    status = Column(
        String(30),
        nullable=False,
        default="Available",
    )