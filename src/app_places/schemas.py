from datetime import datetime as dt
from typing import Optional

from pydantic import BaseModel, Field


class PlaceSearchParams(BaseModel):
    """Схема валидации входящих данных для поиска места"""
    query: Optional[str] = Field(None, description="Поиск места")
    near: Optional[str] = Field(None, description="Город или регион")
    limit: Optional[int] = Field(10, ge=1, le=50,
                                 description="Лимит запроса")


class CategoryOut(BaseModel):
    name: str

    class Config:
        orm_mode = True


class PlaceOut(BaseModel):
    """
    Схема валидации и сериализации выходных данных
    """
    fsq_id: str = Field(..., max_length=100)
    name: str = Field(..., max_length=200)
    address: Optional[str] = Field(None, max_length=300)
    latitude: Optional[float]
    longitude: Optional[float]
    category: Optional[CategoryOut]
    rating: Optional[float] = Field(ge=0, le=10)
    created_at: Optional[dt]
    updated_at: Optional[dt] = None

    class Config:
        orm_mode = True
