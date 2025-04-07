from typing import List

from pydantic import BaseModel, ConfigDict

class NewLocationWKT(BaseModel):
    coordinates: str

class LocationCreate(BaseModel):
    latitude: float
    longitude: float

class LocationUpdate(BaseModel):
    pass

class LocationDB(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    latitude: float
    longitude: float

class LocationsDB(BaseModel):
    locations: List[LocationDB]
