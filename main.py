from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import List

from src.app_places.db import Base, engine, get_db
from src.app_places.models import Place, Category
from src.app_places.schemas import PlaceSearchParams, PlaceOut
from src.app_places.router import search_places_from_foursquare


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/search_places", response_model=List[PlaceOut], summary='Поиск мест')
def search_places(
    params: PlaceSearchParams = Depends(),
    db: Session = Depends(get_db),
):
    """Энд поинт запроса в апи"""

    clean_params = {
        "query": params.query,
        "near": params.near,
        "limit": params.limit,
    }
    clean_params = {k: v for k, v in clean_params.items() if v is not None}

    # Получаем данные по API
    api_response = search_places_from_foursquare(clean_params)
    results = api_response.get("results", [])

    # Собираем все fsq_id и названия категорий
    fsq_ids = []
    category_names = set()
    for item in results:
        if fsq_id := item.get("fsq_id"):
            fsq_ids.append(fsq_id)
        if categories := item.get("categories"):
            if category_name := categories[0].get("name"):
                category_names.add(category_name)

    # Проверяем существующие места
    existing_places = {
        row.fsq_id for row in
        db.query(Place.fsq_id).filter(Place.fsq_id.in_(fsq_ids)).all()
    }

    # Обрабатываем категории
    existing_categories = {
        c.name: c for c in
        db.query(Category).filter(Category.name.in_(category_names)).all()
    }

    # Создаем новые категории
    new_categories = [
        Category(name=name)
        for name in category_names
        if name not in existing_categories
    ]
    if new_categories:
        db.bulk_save_objects(new_categories)
        db.flush()  # Для получения ID новых категорий
        existing_categories.update(
            {c.name: c for c in db.query(Category)
             .filter(Category.name.in_([nc.name for nc in new_categories]))
             .all()}
        )

    # Создаем новые места
    new_places = []
    for item in results:
        fsq_id = item.get("fsq_id")
        if not fsq_id or fsq_id in existing_places:
            continue

        # Обработка адреса
        location = item.get("location", {})
        address = location.get("formatted_address") or location.get("address", "")

        # Получаем категорию
        category_id = None
        if categories := item.get("categories"):
            if category_name := categories[0].get("name"):
                category = existing_categories.get(category_name)
                if category:
                    category_id = category.id

        new_place = Place(
            fsq_id=fsq_id,
            name=item.get("name"),
            address=address,
            latitude=item.get("geocodes", {}).get("main", {}).get("latitude"),
            longitude=item.get("geocodes", {}).get("main", {}).get("longitude"),
            rating=item.get("rating"),
            category_id=category_id
        )
        new_places.append(new_place)

    if new_places:
        db.add_all(new_places)
        db.commit()

    return new_places
