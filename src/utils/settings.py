from  pydantic_settings import BaseSettings,SettingsConfigDict

from sqlalchemy.ext.asyncio import  create_async_engine


class Settings(BaseSettings):


    model_config=SettingsConfigDict(env_file=".env",extra="ignore")
    DATABASE_URL:str

settings=Settings()



