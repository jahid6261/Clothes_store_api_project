from sqlalchemy import Column,Integer,String,Text,DateTime
from sqlalchemy.sql import func
from src.utils.db import DBModel


class Category(DBModel):

    __tablename__ = "categories"

    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100),unique=True,nullable=False)
    slug=Column(String(100),unique=True,nullable=False) 
    description =Column(Text,nullable=False)
    
    created_at=Column(DateTime(timezone=True),server_default=func.now()) 
    updated_at=Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())



    
 
    