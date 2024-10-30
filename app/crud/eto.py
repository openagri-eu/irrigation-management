import datetime
from typing import Optional

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from crud.base import CRUDBase, CreateSchemaType, ModelType
from models import Eto, Location
from schemas import EtoCreate, EtoUpdate


class CrudEto(CRUDBase[Eto, EtoCreate, EtoUpdate]):

    def create(self, db: Session, obj_in: EtoCreate, **kwargs) -> Optional[Eto]:
        obj_in_data = obj_in.model_dump()

        location_db = db.query(Location).filter(Location.id == obj_in.location_id).first()

        if not location_db:
            return None

        db_obj = Eto(**obj_in_data)
        db.add(db_obj)
        try:
            db.commit()
        except SQLAlchemyError:
            return None
        db.refresh(db_obj)

        return db_obj

    def get_calculations(self, db: Session, from_date:datetime.date, to_date: datetime.date, location_id: int):
        return db.query(Eto).filter(Eto.location_id == location_id, Eto.date > from_date, Eto.date < to_date).order_by(desc(Eto.date)).all()



eto = CrudEto(Eto)
