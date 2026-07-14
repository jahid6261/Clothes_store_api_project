from  pydantic_settings import BaseSettings,SettingsConfigDict

from sqlalchemy.ext.asyncio import  create_async_engine


class Settings(BaseSettings):


    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    DATABASE_URL:str
    SECRET_KEY:str
    ALGORITHM:str


    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str
    EMAIL_FROM: str
    CELERY_BROKER_URL:str
    BASE_URL:str

settings=Settings()



