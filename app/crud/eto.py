import datetime
from typing import Optional, List

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from crud.base import CRUDBase
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

    def batch_create(self, db: Session, obj_in: List[EtoCreate], **kwargs) -> Optional[List[Eto]]:
        db_objects = []

        location_ids = [l[0] for l in db.query(Location.id).filter(Location.id.in_([x.location_id for x in obj_in])).all()]

        for obj in obj_in:
            obj_in_data = obj.model_dump()

            # continue instead of db.rollback() because if one locations is removed during the job, due to another
            # api call, doesn't mean the rest of the locations shouldn't have updated eto values
            if obj.location_id not in location_ids:
                continue

            db_obj = Eto(**obj_in_data)
            db_objects.append(db_obj)

        db.add_all(db_objects)

        try:
            db.commit()
        except SQLAlchemyError:
            db.rollback()
            return None

        for obj in db_objects:
            db.refresh(obj)

        return db_objects



eto = CrudEto(Eto)
