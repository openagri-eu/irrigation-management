from typing import Optional

from pydantic import BaseModel, ConfigDict


class NewLocation(BaseModel):
    city_name: str
    state_code: Optional[str] = None
    country_code: str

class LocationCreate(NewLocation):
    pass

class LocationUpdate(BaseModel):
    state_code: str

class LocationResponseInformation(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_name: str
    state_code: Optional[str] = None
    country_code: str

