from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = 'Library API'
    API_V1_STR: str = '/api/v1'

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: List[str] = ['*']

    class Config:
        case_sensitive = True
        env_file = '.env'

    def __init__(self, **values):
        super().__init__(**values)
        self.SQLALCHEMY_DATABASE_URI = (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}'
        )


settings = Settings()
