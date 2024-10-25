from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from typing import Any


class Base(DeclarativeBase):
    id: Any
    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class Dataset(Base):
    __tablename__ = "dataset"

    id = Column(Integer, primary_key=True)
    dataset_id = Column(Integer)
    date = Column(String)
    soil_moisture_10 = Column(Float)
    soil_moisture_20 = Column(Float)
    soil_moisture_30 = Column(Float)
    soil_moisture_40 = Column(Float)
    soil_moisture_50 = Column(Float)
    soil_moisture_60 = Column(Float)
    rain = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
