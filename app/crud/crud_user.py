from typing import Optional

from sqlalchemy.orm import Session

from core.security import verify_password, get_password_hash
from crud.base import CRUDBase
from models import User
from schemas import UserCreate, UserUpdate


class CrudUser(CRUDBase[User, UserCreate, UserUpdate]):

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        user_db = self.get_by_email(db, email=email)
        if not user_db:
            return None
        if not verify_password(password, user_db.password):
            return None
        return user_db

    def create(self, db: Session, obj_in: UserCreate, **kwargs) -> User:
        obj_in.password = get_password_hash(obj_in.password)
        return super().create(db=db, obj_in=obj_in, **kwargs)


user = CrudUser(User)
