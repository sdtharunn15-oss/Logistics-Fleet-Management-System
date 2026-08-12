from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String

from app.database import Base


class MaintenanceRecord(Base):
    __tablename__ = "maintenance_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    maintenance_type = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    cost = Column(Float, default=0)
    status = Column(String(30), default="scheduled")

    maintenance_date = Column(DateTime, default=datetime.utcnow)
    completed_date = Column(DateTime, nullable=True)