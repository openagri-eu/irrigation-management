from crud.base import CRUDBase
from models.location import Location
from schemas import LocationCreate, LocationUpdate


class CrudLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):

    pass


location = CrudLocation(Location)
