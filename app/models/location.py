from typing import List

from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import relationship, Mapped

from db.base_class import Base


class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    calculations: Mapped[List["Eto"]] = relationship(back_populates="location", cascade="all, delete-orphan")
