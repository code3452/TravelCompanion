from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import requests


from src.app_places.config import headers, url

from src.app_places.db import Base, engine, SessionLocal
from src.app_places.models import Place
from src.app_places.schemas import PlaceSearchParams


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


@app.get("/search_places", summary='Поиск мест')
def search_places(
    params: PlaceSearchParams = Depends(),
    db: Session = Depends(get_db),
):

    clean_params = params.model_dump(exclude_none=True)

    response = requests.get(url=url,
                            headers=headers,
                            params=clean_params)

    data = response.json()

    for item in data.get("results", []):
        place = Place(
            fsq_id=item.get("fsq_id"),
            name=item.get("name"),
            address="".join(item.get("location", {}).get(
                "formatted_address", [])),
            latitude=item.get("geocodes", {}).get("main", {}).get("latitude"),
            longitude=item.get("geocodes", {}).get("main", {}).get(
                "longitude"),
            category=item.get("categories", [{}])[0].get("name") if item.get(
                "categories") else None
        )
        existing = db.query(Place).filter(Place.fsq_id == place.fsq_id).first()
        if not existing:
            db.add(place)

    db.commit()

    return data
