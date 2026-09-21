from sqlalchemy.orm import Session

from app.models.field import Field
from app.schemas.field import FieldCreate


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