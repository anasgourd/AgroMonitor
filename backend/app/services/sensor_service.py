from sqlalchemy.orm import Session
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor import SensorCreate,SensorUpdate
from app.models.sensor import Sensor


class SensorService:
    def __init__(self, db: Session):
        self.repository = SensorRepository(db)
    
    def get_field_sensors(self,field_id: int) -> list[Sensor]:
        return self.repository.get_by_field_id(field_id)
         
    def create_sensor(
        self,
        field_id: int,
        sensor_data: SensorCreate
    ) -> Sensor:

        return self.repository.create(
            field_id,
            sensor_data
        )
    
    def get_sensor(self,sensor_id: int) -> Sensor | None:

        return self.repository.get_by_id(sensor_id)
    
    def update_sensor(
        self,
        sensor_id: int,
        sensor_data: SensorUpdate
    ) -> Sensor | None:

        return self.repository.update(
            sensor_id,
            sensor_data
        )
        
    def delete_sensor(self, sensor_id: int) -> str:
        sensor = self.repository.get_by_id(sensor_id)

        if sensor is None:
            return "not_found"

        if self.repository.has_measurements(sensor_id):
            return "has_measurements"

        self.repository.delete(sensor_id)

        return "deleted"