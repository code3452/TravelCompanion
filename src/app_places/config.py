import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = "https://api.foursquare.com/v3/places/search"

headers = {
    "Accept": "application/json",
    "Authorization": API_KEY
}

print(API_KEY)
