from sqlalchemy.orm import Session

from app.models.field import Field
from app.schemas.field import FieldCreate

from app.models.sensor import Sensor

class FieldRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        user_id: int,
        field_data: FieldCreate
    ) -> Field:

        field = Field(
            user_id=user_id,
            field_name=field_data.field_name,
            type=field_data.type,
            area=field_data.area,
        )

        self.db.add(field)
        self.db.commit()
        self.db.refresh(field)

        return field
        
    def get_by_user_id(self, user_id: int):
        return self.db.query(Field).filter(Field.user_id == user_id).all()
    

    def get_by_id(self, field_id: int):
        return (
            self.db.query(Field)
            .filter(Field.field_id == field_id)
            .first()
        )
    
    def update(self, field_id: int, field_data):
        field = self.get_by_id(field_id)

        if field is None:
            return None

        field.field_name = field_data.field_name
        field.type = field_data.type
        field.area = field_data.area

        self.db.commit()
        self.db.refresh(field)

        return field
    
    def delete(self, field_id: int):
        field = self.get_by_id(field_id)

        if field is None:
            return False

        self.db.delete(field)
        self.db.commit()

        return True
    
    def has_sensors(self, field_id: int) -> bool:
        return (
            self.db.query(Sensor)
            .filter(Sensor.field_id == field_id)
            .first()
        ) is not None