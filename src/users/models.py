from sqlalchemy import Column,Integer,String,Boolean,DateTime,Enum,func


import enum
from sqlalchemy.orm  import relationship
from src.utils.db import DBModel

class UserRole(enum.Enum):
    admin='admin'
    user='user'


class UserModel(DBModel):

    __tablename__ = "users"

    id=Column(Integer,primary_key=True,index=True )
    first_name=Column(String(100),nullable=False)
    last_name=Column(String(100),nullable=False)
    email=Column(String(255),unique=True,index=True,nullable=False)
    password=Column(String(255),nullable=False)
    number=Column(String(15),index=True,nullable=False)
    address=Column(String(255),nullable=True)

    is_active=Column(Boolean,default=False)
    verification_token=Column(String(250),nullable=True)
    verification_token_expire=Column(DateTime,nullable=True)

    role=Column(Enum(UserRole),default=UserRole.user,nullable=False)


    created_at=Column(DateTime(timezone=True),server_default=func.now()) 
    updated_at=Column(DateTime(timezone=True), server_default=func.now(),onupdate=func.now())
    
    cart=relationship("Cart",back_populates="user")
    orders=relationship("Order",back_populates="user")