from sqlalchemy import Column, Integer, String, ForeignKey
from app.core.base import Base


class Sensor(Base):
    __tablename__ = "sensors"

    sensor_id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.field_id"), nullable=False)
    sensor_name = Column(String, nullable=False)
    status = Column(String, nullable=False)