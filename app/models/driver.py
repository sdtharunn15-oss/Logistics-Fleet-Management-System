from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    experience_years = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)