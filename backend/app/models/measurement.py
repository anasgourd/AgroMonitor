from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String

from app.core.base import Base


class Measurement(Base):
    __tablename__ = "measurements"

    measurement_id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(
        Integer,
        ForeignKey("sensors.sensor_id"),
        nullable=False
    )
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    unit = Column(String, nullable=False)
    is_anomalous = Column(Boolean, nullable=False)