from typing import List

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship, Mapped

from db.base_class import Base


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    city_name = Column(String, nullable=True)
    # State code ONLY for US states
    state_code = Column(String, nullable=True)
    country_code = Column(String, nullable=True)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    calculations: Mapped[List["Eto"]] = relationship(back_populates="location", cascade="all, delete-orphan")
