import requests
from fastapi import APIRouter, Depends, HTTPException
from requests import RequestException
from sqlalchemy.orm import Session

from api import deps
from core import settings
from models import User
from schemas import NewLocation, LocationResponseInformation, Message, LocationCreate
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

    if location_information.state_code and (location_information.country_code.lower() != "us" and location_information.country_code.lower() != "usa"):
        raise HTTPException(
            status_code=400,
            detail="Error, can't have state code with non US country, please either input US/USA as country code"
                   "or remove state code from request."
        )

    if location_information.state_code:
        try:
            response = requests.get(
                url="http://api.openweathermap.org/geo/1.0/direct?q={},{},{}&appid={}".format(location_information.city_name,
                                                                                              location_information.state_code,
                                                                                              location_information.country_code,
                                                                                              settings.OWM_API_KEY)
            )
        except RequestException:
            raise HTTPException(
                status_code=400,
                detail="Error during openweathermap API call, their servers might be down, please try again later"
            )
    else:
        try:
            response = requests.get(
                url="http://api.openweathermap.org/geo/1.0/direct?q={},{}&appid={}".format(
                    location_information.city_name,
                    location_information.country_code,
                    settings.OWM_API_KEY
                )
            )
        except RequestException:
            raise HTTPException(
                status_code=400,
                detail="Error during openweathermap API call, their servers might be down, please try again later"
            )

    if (response.status_code / 100) != 2:
        raise HTTPException(
            status_code=400,
            detail="Error when retrieving geo-location data, please check whether the city name or country code is correct"
        )

    body = response.json()

    if len(body) == 0:
        raise HTTPException(
            status_code=400,
            detail="Error, most likely no such location exists on openweathermap, please check whether the city name or country code is correct"
        )

    crud_location_create_schema = LocationCreate(
        city_name=location_information.city_name,
        state_code=location_information.state_code,
        country_code=location_information.country_code,
        latitude=body[0]["lat"],
        longitude=body[0]["lon"]
    )

    new_location = location.create(db=db, obj_in=crud_location_create_schema)

    if not new_location:
        raise HTTPException(
            status_code=400,
            detail="Error, couldn't create location in database due to issue with database"
        )

    return new_location


@router.delete("/{location_id}", response_model=Message)
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

    location.remove(db=db, id=location_id)

    return Message(
        message="Successfully deleted the location"
    )

@router.get("/{location_id}", response_model=LocationResponseInformation)
def get_location(
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
