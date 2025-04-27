import requests

from fastapi import HTTPException


from src.app_places.config import headers, url


def search_places_from_foursquare(params: dict):
    """Функция get-запроса с параметрами"""

    response = requests.get(url=url,
                            headers=headers,
                            params=params
                            )

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail='Данные не найдены')

    response.raise_for_status()
    return response.json()
