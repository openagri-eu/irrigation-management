from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class NewLocation(BaseModel):
    city_name: str
    state_code: Optional[str] = None
    country_code: str

class NewLocationWKT(BaseModel):
    coordinates: str

class LocationCreate(BaseModel):
    latitude: float
    longitude: float

class LocationUpdate(BaseModel):
    pass

class LocationResponseInformation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    latitude: float
    longitude: float

    city_name: Optional[str]
    state_code: Optional[str]
    country_code: Optional[str]


class LocationsDB(BaseModel):
    locations: List[LocationResponseInformation]
