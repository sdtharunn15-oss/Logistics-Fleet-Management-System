from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer

from app.database import Base


class TrackingRecord(Base):
    __tablename__ = "tracking_records"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    speed = Column(Float, default=0)
    recorded_at = Column(DateTime, default=datetime.utcnow)