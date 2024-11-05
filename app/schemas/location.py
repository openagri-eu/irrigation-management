from typing import Optional

from pydantic import BaseModel, ConfigDict


class NewLocation(BaseModel):
    city_name: str
    state_code: Optional[str] = None
    country_code: str

class LocationCreate(NewLocation):
    latitude: float
    longitude: float

class LocationUpdate(BaseModel):
    pass

class LocationResponseInformation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_name: str
    state_code: Optional[str] = None
    country_code: str

