from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate,UserUpdate


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: UserCreate) -> User:
        user = User(
            username=user_data.username,
            full_name=user_data.full_name,
            password=user_data.password,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def get_user(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.user_id == user_id).first()
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> User | None:
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if user is None:
            return None

        user.username = user_data.username
        user.full_name = user_data.full_name
        user.password = user_data.password

        self.db.commit()
        self.db.refresh(user)

        return user
    def delete_user(self, user_id: int) -> bool:
        user = self.db.query(User).filter(User.user_id == user_id).first()

        if user is None:
            return False

        self.db.delete(user)
        self.db.commit()

        return True