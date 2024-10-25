from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import deps
from models import User
from schemas import NewLocation, LocationResponseInformation
from crud import location

router = APIRouter()

@router.post("/", response_model=LocationResponseInformation)
def add_location(
    location_information: NewLocation,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Add a parcel of land to the database (so that the service knows which locations to query for weather info)
    """

    if location_information.state_code is not None:
        if location_information.country_code.lower() != "us" or location_information.country_code.lower() != "usa":
            raise HTTPException(
                status_code=400,
                detail="Error, can't have state code with non US country, please either input US/USA as country code"
                       "or remove state code from request."
            )

    new_location = location.create(db=db, obj_in=location_information)

    return new_location


@router.delete("/{location_id}", response_model=LocationResponseInformation)
def remove_location(
    location_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Remove a location via ID (this also removes all recordings stored in database for this location)
    """

    location_db = location.get(db=db, id=location_id)

    if location_db is None:
        raise HTTPException(
            status_code=400,
            detail="Location with ID:{} does not exist.".format(location_id)
        )

    location_removed = location.remove(db=db, id=location_id)

    return location_removed

@router.get("/{location_id}", response_model=LocationResponseInformation)
def location_details(
    location_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):

    """
    View a location by ID.
    """

    location_db = location.get(db=db, id=location_id)

    if location_db is None:
        raise HTTPException(
            status_code=400,
            detail="Error, Location with ID:{} does not exist.".format(location_id)
        )

    return location_db
