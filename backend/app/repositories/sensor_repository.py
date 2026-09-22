from sqlalchemy.orm import Session
from app.models.sensor import Sensor
from app.models.sensor import Sensor
from app.schemas.sensor import SensorCreate,SensorUpdate


class SensorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_field_id(
        self,
        field_id: int
    ) -> list[Sensor]:

        return (
            self.db.query(Sensor)
            .filter(Sensor.field_id == field_id)
            .all()
        )

    def create(
        self,
        field_id: int,
        sensor_data: SensorCreate
    ) -> Sensor:

        sensor = Sensor(
            field_id=field_id,
            sensor_name=sensor_data.sensor_name,
            status=sensor_data.status,
        )

        self.db.add(sensor)
        self.db.commit()
        self.db.refresh(sensor)

        return sensor
    
    def get_by_id(
        self,
        sensor_id: int
    ) -> Sensor | None:

        return (
            self.db.query(Sensor)
            .filter(Sensor.sensor_id == sensor_id)
            .first()
        )
    
    def update(
    self,
    sensor_id: int,
    sensor_data: SensorUpdate
    ) -> Sensor | None:

        sensor = self.get_by_id(sensor_id)

        if sensor is None:
            return None

        sensor.sensor_name = sensor_data.sensor_name
        sensor.status = sensor_data.status

        self.db.commit()
        self.db.refresh(sensor)

        return sensor
    
    def delete(
        self,
        sensor_id: int
    ) -> bool:

        sensor = self.get_by_id(sensor_id)

        if sensor is None:
            return False

        self.db.delete(sensor)
        self.db.commit()

        return True
