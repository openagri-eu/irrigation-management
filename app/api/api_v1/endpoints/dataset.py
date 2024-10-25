from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from schemas import DatasetAnalysis
from schemas import Dataset as DatasetScheme
from db import get_db
from crud import get_datasets, add_dataset, delete_datasets
from utils import (min_max_date, detect_irrigation_events, count_precipitation_events,
                   count_high_dose_irrigation_events, get_high_dose_irrigation_events_dates, calculate_field_capacity,
                   calculate_stress_level, get_stress_count, get_stress_dates,
                   no_of_saturation_days, get_saturation_dates)

from core import Settings, get_settings


router = APIRouter()

@router.post("/")
def load_dataset(dataset: DatasetScheme, db: Session = Depends(get_db)) -> DatasetScheme:
    return add_dataset(db, dataset)


@router.get("/{dataset_id}")
async def get_dataset(dataset_id: int, db: Session = Depends(get_db)) -> list[DatasetScheme]:
    db_dataset = get_datasets(db, dataset_id)
    if not db_dataset:
        raise HTTPException(status_code=404, detail="No datasets with that id")
    return db_dataset

@router.delete("/{dataset_id}")
def remove_dataset(dataset_id: int, db: Session = Depends(get_db)):
    try:
        deleted = delete_datasets(db, dataset_id)
    except:
        raise HTTPException(status_code=400, detail="Could not delete dataset")

    if deleted == 0:
        raise HTTPException(status_code=400, detail="No dataset with given id")
    return {"status_code":201, "detail": "Successfully deleted"}

@router.get("/{dataset_id}/analysis")
def analyse_soil_moisture(dataset_id: int, db: Session = Depends(get_db),
                                           settings: Settings = Depends(get_settings)) -> DatasetAnalysis:
    dataset: list[DatasetScheme] = get_datasets(db, dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    result = DatasetAnalysis

    result.dataset_id = dataset_id
    result.time_period = min_max_date(dataset)
    result.irrigation_events_detected = detect_irrigation_events(dataset, settings)
    result.precipitation_events = count_precipitation_events(dataset, settings)
    result.high_dose_irrigation_events = count_high_dose_irrigation_events(dataset, settings)
    result.high_dose_irrigation_events_dates = get_high_dose_irrigation_events_dates(dataset, settings)
    field_capacity = calculate_field_capacity(dataset)
    result.field_capacity = field_capacity
    stress_level = calculate_stress_level(field_capacity)
    result.stress_level = stress_level
    result.number_of_saturation_days = no_of_saturation_days(dataset, field_capacity, settings)
    result.saturation_dates = get_saturation_dates(dataset, field_capacity, settings)
    result.no_of_stress_days = get_stress_count(dataset, stress_level)
    result.stress_dates = get_stress_dates(dataset, stress_level)

    return result