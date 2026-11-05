
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User
from app.core.security import hash_password


class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(self, user_data: UserCreate) -> User:
        existing_user = self.repository.get_by_username(
            user_data.username
        )

        if existing_user is not None:
            raise HTTPException(
                status_code=409,
                detail="Username already exists"
            )

        hashed_data = user_data.model_copy(
            update={
                "password": hash_password(user_data.password)
            }
        )

        try:
            return self.repository.create(hashed_data)
        except IntegrityError as exc:
            self.db.rollback()

            if self.repository.get_by_username(
                user_data.username
            ) is not None:
                raise HTTPException(
                    status_code=409,
                    detail="Username already exists"
                ) from exc

            raise

    def get_user(self, user_id: int) -> User:
        return self.repository.get_user(user_id)

    def update_user(
        self, user_id: int, user_data: UserUpdate
    ) -> User | None:
        user_data.password = hash_password(user_data.password)
        return self.repository.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete_user(user_id)
