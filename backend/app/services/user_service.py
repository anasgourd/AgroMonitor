from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate,UserUpdate
from app.models.user import User
from app.core.security import hash_password


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        # Password hashing added.
        hashed_password = hash_password(user_data.password)
        
        user_data.password = hashed_password

        return self.repository.create(user_data)
        
    def get_user(self,user_id: int) -> User:
        return self.repository.get_user(user_id)
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        user_data.password = hash_password(user_data.password)

        return self.repository.update_user(user_id, user_data)
    
    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete_user(user_id)