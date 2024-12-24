from typing import Annotated

import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from core import security
from core.security import *
from core.config import settings
from api import deps
from crud import user
from schemas import Token

router = APIRouter()


@router.post("/access-token/", response_model=Token)
def login_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(deps.get_db)
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    if not settings.USING_GATEKEEPER:


        user_db = user.authenticate(
            db, email=form_data.username, password=form_data.password
        )

        if not user_db:
            raise HTTPException(status_code=400, detail="Incorrect email or password")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION_TIME)

        at = Token(access_token=security.create_access_token(
                user_db.id, expires_delta=access_token_expires
            ),
            token_type="bearer"
        )
    else:
        response = requests.post(
            url=settings.GATEKEEPER_BASE_URL.unicode_string() + "api/login/",
            headers={"Content-Type": "application/json"},
            json={"username": "{}".format(form_data.username), "password": "{}".format(form_data.password)}
        )

        if response.status_code == 401:
            raise HTTPException(
                status_code=400,
                detail="Error, no active account found with these credentials."
            )

        at = Token(
            access_token=response.json()["access"],
            token_type="bearer"
        )

    return at
