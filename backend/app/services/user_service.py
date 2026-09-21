from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate,UserUpdate
from app.models.user import User



class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        # Password hashing will be added here.
        return self.repository.create(user_data)
        
    def get_user(self,user_id: int) -> User:
        return self.repository.get_user(user_id)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        return self.repository.update_user(user_id, user_data)
    
    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete_user(user_id)