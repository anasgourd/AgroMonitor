from datetime import datetime

from pydantic import BaseModel, Field


class MeasurementInput(BaseModel):
    sensor_id: int = Field(gt=0)
    value: float = Field(allow_inf_nan=False)
    timestamp: datetime
    unit: str



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