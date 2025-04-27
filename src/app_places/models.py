from sqlalchemy import (Column, Integer, String,
                        Float, DateTime, func, ForeignKey)
from sqlalchemy.orm import relationship
from src.app_places.db import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True,
                comment="Уникальный Id Категории")
    name = Column(String, unique=True, nullable=False,
                  comment='Название категории')

    places = relationship("Place", back_populates="category")


class Place(Base):
    """ Модель хранения мест в бд """
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True,
                comment="Уникальный ID места")
    fsq_id = Column(String(100), unique=True, index=True,
                    comment="ID места в Foursquare")
    name = Column(String(200), comment="Название места")
    address = Column(String(300), comment='Адрес места')
    latitude = Column(Float, comment='Широта')
    longitude = Column(Float, comment='Долгота')
    category_id = Column(Integer, ForeignKey("categories.id"), index=True)
    category = relationship("Category", back_populates="places")
    rating = Column(Float, comment="Рейтинг места")
    created_at = Column(DateTime(timezone=True), server_default=func.now(),
                        comment='Дата и время создания записи')
    update_at = Column(DateTime(timezone=True), onupdate=func.now(),
                       server_default=func.now(),
                       comment='Дата и время последнего обновления')
