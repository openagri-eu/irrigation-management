from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from api.deps import get_db
from schemas import DatasetAnalysis
from schemas import Dataset as DatasetScheme
from crud import dataset as crud_dataset
from utils import (min_max_date, detect_irrigation_events, count_precipitation_events,
                   count_high_dose_irrigation_events, get_high_dose_irrigation_events_dates, calculate_field_capacity,
                   calculate_stress_level, get_stress_count, get_stress_dates,
                   no_of_saturation_days, get_saturation_dates)



router = APIRouter()


@router.post("/", response_model=DatasetScheme)
def load_dataset(
        dataset: DatasetScheme,
        db: Session = Depends(get_db)
) -> DatasetScheme:
    return crud_dataset.add_dataset(db, dataset)


@router.get("/{dataset_id}", response_model=List[DatasetScheme])
async def get_dataset(
        dataset_id: int,
        db: Session = Depends(get_db)
) -> list[DatasetScheme]:
    db_dataset = crud_dataset.get_datasets(db, dataset_id)
    if not db_dataset:
        raise HTTPException(status_code=404, detail="No datasets with that id")
    return db_dataset


@router.delete("/{dataset_id}")
def remove_dataset(
        dataset_id: int,
        db: Session = Depends(get_db)
):
    try:
        deleted = crud_dataset.delete_datasets(db, dataset_id)
    except:
        raise HTTPException(status_code=400, detail="Could not delete dataset")

    if deleted == 0:
        raise HTTPException(status_code=400, detail="No dataset with given id")
    return {"status_code":201, "detail": "Successfully deleted"}


@router.get("/{dataset_id}/analysis", response_model=DatasetAnalysis)
def analyse_soil_moisture(
        dataset_id: int,
        db: Session = Depends(get_db)
) -> DatasetAnalysis:
    dataset: list[DatasetScheme] = crud_dataset.get_datasets(db, dataset_id)

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    field_capacity = calculate_field_capacity(dataset)
    stress_level = calculate_stress_level(field_capacity)

    result = DatasetAnalysis(
        dataset_id=dataset_id,
        time_period=min_max_date(dataset),
        irrigation_events_detected=detect_irrigation_events(dataset),
        precipitation_events=count_precipitation_events(dataset),
        high_dose_irrigation_events=count_high_dose_irrigation_events(dataset),
        high_dose_irrigation_events_dates=get_high_dose_irrigation_events_dates(dataset),
        field_capacity=field_capacity,
        stress_level=stress_level,
        number_of_saturation_days=no_of_saturation_days(dataset, field_capacity),
        saturation_dates=get_saturation_dates(dataset, field_capacity),
        no_of_stress_days=get_stress_count(dataset, stress_level),
        stress_dates=get_stress_dates(dataset, stress_level)

    )

    return result
