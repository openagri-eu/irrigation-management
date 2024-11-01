from sqlalchemy import Column, Integer, String

from db.base_class import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String,  index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
