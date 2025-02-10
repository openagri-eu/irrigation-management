import requests
from fastapi import APIRouter, Depends, HTTPException
from requests import RequestException
from shapely import wkt, errors
from sqlalchemy.orm import Session

from api import deps
from core import settings
from models import User
from schemas import NewLocation, LocationResponseInformation, Message, LocationCreate, NewLocationWKT, LocationsDB
from crud import location

router = APIRouter()

@router.post("/", response_model=Message)
def add_location(
    location_information: NewLocation,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Message:
    """
    Add a parcel of land to the database (so that the service knows which locations to query for weather info)
    """

    if location_information.state_code and (location_information.country_code.lower() != "us" and location_information.country_code.lower() != "usa"):
        raise HTTPException(
            status_code=400,
            detail="Error, can't have state code with non US country, please either input US/USA as country code"
                   "or remove state code from request."
        )

    url = "http://api.openweathermap.org/geo/1.0/direct?q={},{}&appid={}".format(
        location_information.city_name,
        location_information.country_code,
        settings.OWM_API_KEY
    )

    if location_information.state_code:
        url = "http://api.openweathermap.org/geo/1.0/direct?q={},{},{}&appid={}".format(location_information.city_name,
                                                                                        location_information.state_code,
                                                                                        location_information.country_code,
                                                                                        settings.OWM_API_KEY)

    try:
        response = requests.get(url)
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
        latitude=body[0]["lat"],
        longitude=body[0]["lon"]
    )

    new_location = location.create(db=db, obj_in=crud_location_create_schema)

    if not new_location:
        raise HTTPException(
            status_code=400,
            detail="Error, couldn't create location in database due to issue with database"
        )

    return Message(message="Successfully created new location!")

@router.post("/parcel-wkt/", response_model=Message)
def add_location_wkt(
    location_information: NewLocationWKT,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
) -> Message:
    """
    Add a new location based on parcel information (wkt format)

    An example of a parcel represented with wkt:
    POLYGON ((40.2 21.2, 40.3 21.3, 40.5 25.2, 36.1 23.1, 40.2 21.2))
    """

    try:
        base_geometry = wkt.loads(location_information.coordinates)
    except errors.ShapelyError as se:
        raise HTTPException(
            status_code=400,
            detail="Error during WKT parsing, please check format, floats,"
                   " that it encompasses a closed structure. Specific exception information: [{}]".format(se)
        )

    c_latitude = base_geometry.centroid.x
    c_longitude = base_geometry.centroid.y

    # Check whether opentopo returns an elevation
    try:
        response_otd = requests.get(
            url="https://api.opentopodata.org/v1/{}?locations={},{}".format("eudem25m", c_latitude, c_longitude)
        )
    except RequestException:
        raise HTTPException(
            status_code=400,
            detail="Error, can't check topographical location of wkt parcel, please try again later."
        )

    if (response_otd.status_code / 100) != 2:
        raise HTTPException(
            status_code=400,
            detail="Error, topographical api issue, please try again later."
        )

    body = response_otd.json()

    if "results" not in body:
        raise HTTPException(
            status_code=400,
            detail="Error, topographical api failed to return a result, please try again later."
        )

    if len(body["results"]) == 0:
        raise HTTPException(
            status_code=400,
            detail="Error, topographical api returned an empty results set, please try again later."
        )

    if "elevation" not in body["results"][0]:
        raise HTTPException(
            status_code=400,
            detail="Error, elevation data missing from topographical api call, please try again later."
        )

    if not body["results"][0]["elevation"]:
        raise HTTPException(
            status_code=400,
            detail="Error, wkt coordinates do not point to a European location, only European continental parcels "
                   "are supported currently."
        )

    location.create(db=db, obj_in=LocationCreate(latitude=float(c_latitude), longitude=float(c_longitude)))

    return Message(message="Successfully created new location!")


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

@router.get("/", response_model=LocationsDB)
def get_all(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all locations
    """

    locations = location.get_all(db=db)

    return LocationsDB(locations=locations)
