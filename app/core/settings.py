from functools import lru_cache

from typing import List
from pydantic import BaseSettings, AnyHttpUrl

class Settings(BaseSettings):
    DATABASE_URL : str = "sqlite:///./sql_app.db"
    ACCESS_TOKEN_EXPIRE_MINUTES : int = 30
    JWT_SECRET : str = "JWTSEGREDO"
    ALGORITHM : str = "HS256"

    SOCKET_SERVER_ADDRESS: str = "https://zrp-challenge-socket.herokuapp.com"
    SOCKET_EVENT_NAME: str = "occurrence"

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8001"
    ]

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()