from datetime import datetime

from pydantic import BaseModel


class AlertResponse(BaseModel):
    alert_id: int
    measurement_id: int
    message: str
    timestamp: datetime

    model_config = {
        "from_attributes": True
    }