from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
import crud

from models import User
from schemas import EToRequest, EToResponse


router = APIRouter()


@router.post("/get-calculations/{location_id}", response_model=EToResponse)
def get_calculations(
    location_id: int,
    er: EToRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Returns ETo calculations for the requested days
    """

    if er.from_date > er.to_date:
        raise HTTPException(
            status_code=400,
            detail="Error, from date can't be later than to date"
        )

    location_db = crud.location.get(db=db, id=location_id)

    if location_db is None:
        raise HTTPException(
            status_code=400,
            detail="Error, location with ID:{} does not exist.".format(location_id)
        )

    return EToResponse(
        calculations=crud.eto.get_calculations(
            db=db,
            from_date=er.from_date,
            to_date=er.to_date,
            location_id=location_id
        )
    )
