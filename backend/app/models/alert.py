from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from app.core.base import Base


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    measurement_id = Column(
        Integer,
        ForeignKey("measurements.measurement_id"),
        nullable=False,
        unique=True
        #each measurement can give one anomaly so one alert
    )
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)