from typing import List

from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models.location import Location
from schemas import LocationCreate, LocationUpdate


class CrudLocation(CRUDBase[Location, LocationCreate, LocationUpdate]):

    def get_all(self, db: Session) -> List[Location]:
        return db.query(Location).all()


location = CrudLocation(Location)
