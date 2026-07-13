

from datetime import datetime

from pydantic import BaseModel,EmailStr
from src.users.models import UserRole


class UserRegisterSchema(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    number:str
    address:str|None=None


class UserLoginSchema(BaseModel):
    email:EmailStr
    password:str

class TokenSchema(BaseModel):
    access_token:str
    token_type:str="bearer"


class UserResponseSchema(BaseModel):

    id:int
    first_name:str
    last_name:str
    email:EmailStr
    number:str
    address:str
    role:UserRole
    is_active:bool
    created_at:datetime
    updated_at:datetime


