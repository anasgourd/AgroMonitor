from datetime import datetime

from pydantic import BaseModel


class MeasurementResponse(BaseModel):
    measurement_id: int
    sensor_id: int
    value: float
    timestamp: datetime
    unit: str
    is_anomalous: bool

    model_config = {
        "from_attributes": True
    }