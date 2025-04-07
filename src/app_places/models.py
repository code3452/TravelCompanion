from sqlalchemy import Column, Integer, String, Float
from src.app_places.db import Base


class Place(Base):
    """ Модель хранения мест в бд """
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    fsq_id = Column(String, unique=True, index=True)
    name = Column(String)
    address = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    category = Column(String)
