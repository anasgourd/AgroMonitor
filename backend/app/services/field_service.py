from sqlalchemy.orm import Session
from app.repositories.field_repository import FieldRepository
from app.models.field import Field
from app.schemas.field import FieldCreate

class FieldService:

    def __init__(self, db: Session):
        self.repository = FieldRepository(db)
        
    def create_field(
        self,
        user_id: int,
        field_data: FieldCreate
    ) -> Field:

        return self.repository.create(user_id, field_data)
        
    
    def get_user_fields(self, user_id: int) -> list[Field]  | None:

        return self.repository.get_by_user_id(user_id)
    
    def get_field(self, field_id: int):
        return self.repository.get_by_id(field_id)
    def update_field(self, field_id: int, field_data):
        return self.repository.update(field_id, field_data)

    def delete_field(self, field_id: int) -> str:
        field = self.repository.get_by_id(field_id)

        if field is None:
            return "not_found"

        if self.repository.has_sensors(field_id):
            return "has_sensors"

        self.repository.delete(field_id)

        return "deleted"
    