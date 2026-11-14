from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def login(self, username: str, password: str) -> str | None:
        user = self.repository.get_by_username(username)

        if user is None:
            return None

        if not verify_password(password, user.password):
            return None

        return create_access_token(user.user_id)