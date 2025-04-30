import os
from dotenv import load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env",
                                      env_file_encoding="utf-8")


settings = Settings()

load_dotenv()

API_KEY = os.getenv('API_KEY')

url = os.getenv('URL')


headers = {
    "Accept": "application/json",
    "Authorization": API_KEY
}
