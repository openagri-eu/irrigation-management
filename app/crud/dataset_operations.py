from sqlalchemy.orm import Session

from crud.base import CRUDBase
from models import Dataset as DM
from schemas import Dataset as DS


class CrudDataset(CRUDBase[DM, DS, dict]):

    def add_dataset(self, db: Session, dataset: DS):
        db_dataset = DM(dataset_id = dataset.dataset_id,
                        date = dataset.date,
                        soil_moisture_10 = dataset.soil_moisture_10,
                        soil_moisture_20 = dataset.soil_moisture_20,
                        soil_moisture_30 = dataset.soil_moisture_30,
                        soil_moisture_40 = dataset.soil_moisture_40,
                        soil_moisture_50 = dataset.soil_moisture_50,
                        soil_moisture_60 = dataset.soil_moisture_60,
                        rain = dataset.rain,
                        temperature = dataset.temperature,
                        humidity = dataset.humidity)
        db.add(db_dataset)
        db.commit()
        db.refresh(db_dataset)
        return db_dataset


    def get_datasets(self, db: Session, dataset_id: int):
        return db.query(DM).filter(DM.dataset_id == dataset_id).all()


    def delete_datasets(self, db: Session, dataset_id:int):
        deleted = db.query(DM).filter_by(dataset_id=dataset_id).delete()
        db.commit()
        return deleted


dataset = CrudDataset(DM)
