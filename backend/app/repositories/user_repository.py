from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


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