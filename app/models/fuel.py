from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from datetime import datetime

from app.database import Base


class FuelRecord(Base):
    __tablename__ = "fuel_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    fuel_type = Column(String(30), default="diesel")
    quantity_liters = Column(Float, nullable=False)
    price_per_liter = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)

    odometer = Column(Float, default=0)
    fuel_date = Column(DateTime, default=datetime.utcnow)