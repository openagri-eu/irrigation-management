from typing import Generator

import requests

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from models import User
from crud import user

from core import security
from core.config import settings
from db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token/")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: Session = Depends(get_db),
        token: str = Depends(reusable_oauth2)
) -> User:
    if settings.USING_GATEKEEPER:
        response = requests.post(
            url=settings.GATEKEEPER_BASE_URL.unicode_string() + "api/validate_token/",
            headers={"Content-Type": "application/json"},
            json={"token": token, "token_type": "access"}
        )

        if response.status_code == 400:
            raise HTTPException(
                status_code=400,
                detail="Error, bad jwt token."
            )

        return User(email=token)

    else:
        try:
            payload = jwt.decode(
                token, settings.JWT_KEY, algorithms=[security.ALGORITHM]
            )
        except (jwt.PyJWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )

        user_db = user.get(db, id=payload["sub"])

        if not user_db:
            raise HTTPException(status_code=404, detail="User not found")

        return user_db
