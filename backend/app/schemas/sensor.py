from pydantic import BaseModel




class SensorCreate(BaseModel):
    sensor_name: str
    status: str
    
class SensorUpdate(BaseModel):
    sensor_name: str
    status: str
    
class SensorResponse(BaseModel):
    sensor_id: int
    field_id: int
    sensor_name: str
    status: str

    model_config = {
        "from_attributes": True
    }