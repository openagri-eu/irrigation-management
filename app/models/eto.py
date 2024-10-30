from sqlalchemy import Column, Integer, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base_class import Base


class Eto(Base):
    __tablename__ = 'eto'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)

    date = Column(Date, nullable=False)
    value = Column(Float, nullable=False)

    location_id: Mapped[int] = mapped_column(ForeignKey("location.id"))
    location: Mapped["Location"] = relationship(back_populates="calculations")
