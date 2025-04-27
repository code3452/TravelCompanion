import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = os.getenv('URL')


headers = {
    "Accept": "application/json",
    "Authorization": API_KEY
}
