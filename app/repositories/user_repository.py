from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    def create(self, db: Session, data: UserCreate) -> User:
        user = User(email=data.email.lower(), hashed_password=hash_password(data.password))
        db.add(user)
        db.flush()
        return user

    def get_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email.lower()).first()

    def get_by_id(self, db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.id == user_id).first()
