from pydantic import BaseModel, Field
from typing import Optional


class PlaceSearchParams(BaseModel):
    query: Optional[str] = Field(None, description="Поиск места")
    near: Optional[str] = Field(None, description="Город или регион")
    limit: Optional[int] = Field(10, ge=1, le=50,
                                 description="Лимит запроса")
