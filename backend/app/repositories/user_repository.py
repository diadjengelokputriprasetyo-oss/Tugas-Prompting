from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email.lower().strip()).first()

    def create(self, user_data: dict) -> User:
        user = User(
            full_name=user_data["full_name"],
            email=user_data["email"].lower().strip(),
            password_hash=user_data["password_hash"],
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list(self, limit: int = 10, offset: int = 0) -> List[User]:
        return self.db.query(User).offset(offset).limit(limit).all()
